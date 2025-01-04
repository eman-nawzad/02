import streamlit as st
import geopandas as gpd
import rasterio
import numpy as np
from folium import Map
from folium.raster_layers import ImageOverlay
from matplotlib import cm
from streamlit_folium import st_folium

# App title
st.title("Drought Monitoring Web Application")

# Sidebar header
st.sidebar.header("Map Customization")

# User controls in the sidebar
map_zoom = st.sidebar.slider("Map Zoom Level", min_value=1, max_value=18, value=8)

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

# Mask no-data values
@st.cache_data
def mask_no_data(profile, data):
    no_data_value = profile.get('nodata')
    if no_data_value is not None:
        data = np.ma.masked_equal(data, no_data_value)
    return data

# Load SPI data
spi_file = "SPI_12.tif"  # SPI GeoTIFF file
spi_data, bounds, profile = load_spi_data(spi_file)
st.sidebar.write("SPI Data Loaded Successfully!")

# Mask the SPI data
masked_spi = mask_no_data(profile, spi_data)

# Normalize SPI data for display
normalized_spi = normalize_data(masked_spi)

# Create a folium map
center_lat = (bounds.top + bounds.bottom) / 2
center_lon = (bounds.left + bounds.right) / 2
m = Map(location=[center_lat, center_lon], zoom_start=map_zoom, tiles="OpenStreetMap")

# Apply custom colors to the map visualization
colormap = cm.get_cmap("coolwarm")
rgba_data = colormap(normalized_spi)
rgba_data = (rgba_data[:, :, :3] * 255).astype(np.uint8)  # Convert to RGB format

# Set alpha channel to 0 (transparent) for no-data values
alpha_channel = np.zeros_like(rgba_data[:, :, 0], dtype=np.uint8)
alpha_channel[~np.isnan(masked_spi)] = 255  # Set alpha to 255 (opaque) where data is not masked
rgba_data = np.dstack((rgba_data, alpha_channel))

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

# Display the map
st.header("Interactive Map with OpenStreetMap Basemap")
st_folium(m, width=800, height=500)






















