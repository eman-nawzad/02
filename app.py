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
spi_file = "SPI_12_2023.tif"  # SPI GeoTIFF file
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

# Create the color legend for the map
def add_legend(map_obj):
    legend_html = """
        <div style="position: fixed; 
                    bottom: 10px; left: 10px; width: 160px; height: 130px; 
                    background-color: white; border:2px solid grey; 
                    z-index:9999; font-size:14px;">
            <div style="padding: 10px;">
                <strong>SPI Legend</strong><br>
                <i style="background: #67001f; width: 20px; height: 20px; display: inline-block; border-radius: 3px;"></i> Extreme Drought (-2.00)<br>
                <i style="background: #f7f4f9; width: 20px; height: 20px; display: inline-block; border-radius: 3px;"></i> Mild Drought (0.00)<br>
                <i style="background: #b2182b; width: 20px; height: 20px; display: inline-block; border-radius: 3px;"></i> Moderate Drought (-1.00 to -1.49)<br>
                <i style="background: #fdae61; width: 20px; height: 20px; display: inline-block; border-radius: 3px;"></i> Severe Drought (-1.50 to -1.99)<br>
            </div>
        </div>
    """
    legend = folium.Element(legend_html)
    map_obj.get_root().html.add_child(legend)

# Add the legend to the map
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



















