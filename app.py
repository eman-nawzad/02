import streamlit as st
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import folium
import numpy as np
from folium.raster_layers import ImageOverlay
from matplotlib import cm
from streamlit_folium import st_folium  # Import for Folium integration in Streamlit

# App title
st.title("Drought Monitoring Web Application")

# Sidebar header
st.sidebar.header("Map Customization")

# Adjust width of the sidebar to be more compact
st.sidebar.markdown('<style> .css-1d391kg {width: 200px;}</style>', unsafe_allow_html=True)

# User controls in the sidebar
map_zoom = st.sidebar.slider("Map Zoom Level", min_value=1, max_value=18, value=8)  # Control zoom level

# Load SPI GeoTIFF data
@st.cache_data
def load_spi_data(file):
    with rasterio.open(file) as src:
        data = src.read(1)  # Read the first band
        bounds = src.bounds  # Get bounding box
        profile = src.profile  # Get metadata
    return data, bounds, profile

# Normalize data for visualization
def normalize_data(data):
    data_min, data_max = np.nanmin(data), np.nanmax(data)
    return (data - data_min) / (data_max - data_min)

# Mask no-data values (assuming the black background is due to no-data values)
@st.cache_data
def mask_no_data(_profile, data):  # Renamed '_profile' to prevent caching issues
    no_data_value = _profile.get('nodata')
    if no_data_value is not None:
        data = np.ma.masked_equal(data, no_data_value)
    return data

# Load GeoJSON or Shapefile
@st.cache_data
def load_vector_data(vector_file):
    return gpd.read_file(vector_file)

# Load SPI data
spi_file = "SPI_12.tif"  # SPI GeoTIFF file
spi_data, bounds, profile = load_spi_data(spi_file)
st.sidebar.write("SPI Data Loaded Successfully!")

# Mask the SPI data
masked_spi = mask_no_data(profile, spi_data)  # Pass 'profile' and 'data' separately

# Normalize SPI data for display
normalized_spi = normalize_data(masked_spi)

# Create a folium map
center_lat = (bounds.top + bounds.bottom) / 2
center_lon = (bounds.left + bounds.right) / 2
m = folium.Map(location=[center_lat, center_lon], zoom_start=map_zoom, tiles="OpenStreetMap")

# Apply custom colors to the map visualization
colormap = cm.get_cmap("coolwarm")  # Use the same colormap as before
rgba_data = colormap(normalized_spi)  # Apply colormap to normalized data
rgba_data = (rgba_data[:, :, :3] * 255).astype(np.uint8)  # Convert to RGB format

# Image overlay for the map
image_overlay = ImageOverlay(
    image=rgba_data,
    bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
    opacity=1,
    interactive=True,
    cross_origin=True,
    zindex=1,
)
image_overlay.add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Function to add professional legend
def add_legend(map_obj):
    legend_html = """
        <div style="position: fixed; 
                    bottom: 100px; left: 10px; width: 220px; height: auto; 
                    background-color: white; border:2px solid grey; 
                    border-radius: 10px; padding: 10px; font-size:14px; z-index: 9999; font-family: Arial, sans-serif;">
            <strong style="font-size:16px;">SPI Legend</strong><br><br>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background: #67001f; border-radius: 3px;"></div>
                <span>&nbsp; Extreme Drought (-2.00)</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background: #f7f4f9; border-radius: 3px;"></div>
                <span>&nbsp; Mild Drought (0.00)</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background: #b2182b; border-radius: 3px;"></div>
                <span>&nbsp; Moderate Drought (-1.00 to -1.49)</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background: #fdae61; border-radius: 3px;"></div>
                <span>&nbsp; Severe Drought (-1.50 to -1.99)</span>
            </div>
        </div>
    """
    legend = folium.Element(legend_html)
    map_obj.get_root().html.add_child(legend)

# Add the professional legend to the map
add_legend(m)

# Display the map
st.header("Interactive Map with OpenStreetMap Basemap")
st_folium(m, width=800, height=500)

# Sidebar information
st.sidebar.info(
    """
    - Customize the map zoom level 
    - The SPI map is visualized on top of an OpenStreetMap basemap.
    """
)






















