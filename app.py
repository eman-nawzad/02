import streamlit as st
import geopandas as gpd
import rasterio
import folium
from rasterio.mask import mask
from folium.raster_layers import ImageOverlay
import numpy as np
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

# Categorize drought thresholds with custom colors
def categorize_drought(data):
    categories = np.empty_like(data, dtype=object)
    categories[data < -2.00] = "Extreme drought"
    categories[(data >= -1.99) & (data <= -1.50)] = "Severe drought"
    categories[(data >= -1.49) & (data <= -1.00)] = "Moderate drought"
    categories[(data >= -0.99) & (data <= 0.00)] = "Mild drought"
    return categories

# Normalize data for visualization
def normalize_data(data):
    data_min, data_max = np.nanmin(data), np.nanmax(data)
    return (data - data_min) / (data_max - data_min)

# Load GeoJSON or Shapefile
@st.cache_data
def load_vector_data(vector_file):
    return gpd.read_file(vector_file)

# Load SPI data
spi_file = "SPI_12_2023.tif"  # SPI GeoTIFF file
spi_data, bounds, profile = load_spi_data(spi_file)
st.sidebar.write("SPI Data Loaded Successfully!")

# Mask no-data values (assuming the black background is due to no-data values)
no_data_value = profile.get('nodata')
if no_data_value is not None:
    spi_data = np.ma.masked_equal(spi_data, no_data_value)

# Normalize SPI data for display
normalized_spi = normalize_data(spi_data)

# Create a folium map
center_lat = (bounds.top + bounds.bottom) / 2
center_lon = (bounds.left + bounds.right) / 2
m = folium.Map(location=[center_lat, center_lon], zoom_start=map_zoom, tiles="OpenStreetMap")

# Apply custom colors to the map visualization
colormap = cm.get_cmap("coolwarm")  # Use the same colormap as before
rgba_data = colormap(normalized_spi)  # Apply colormap to normalized data

# Ensure proper transparency for no-data (by setting alpha to 0 for masked pixels)
rgba_data = (rgba_data[:, :, :3] * 255).astype(np.uint8)  # Convert to RGB format
rgba_data[spi_data.mask] = [0, 0, 0]  # Set masked/no-data regions to black (can be changed to white or transparent)

# ImageOverlay to add the SPI data as an image layer on top of the map
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

# Display the map
st.header("Interactive Map with OpenStreetMap Basemap")
st_folium(m, width=800, height=500)

# Sidebar info
st.sidebar.info(
    """
    - Customize the map zoom level
    - The SPI map is visualized on top of an OpenStreetMap basemap.
    """
)














