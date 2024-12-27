import streamlit as st
import rasterio
import folium
from streamlit_folium import st_folium
import numpy as np

# Title
st.title("Drought Monitoring App")

# Load SPI GeoTIFF file
file_path = "SPI_12_2023.tif"
st.sidebar.header("SPI File")
st.sidebar.text(file_path)

# Read and display the SPI data
with rasterio.open(file_path) as src:
    spi_data = src.read(1)
    transform = src.transform

    # Display basic metadata
    st.sidebar.subheader("File Information")
    st.sidebar.text(f"Width: {src.width}")
    st.sidebar.text(f"Height: {src.height}")
    st.sidebar.text(f"CRS: {src.crs}")

    # Mask invalid values
    spi_data = np.ma.masked_where(spi_data == src.nodata, spi_data)

# Add map
st.subheader("SPI Drought Map")
m = folium.Map(location=[35, 44], zoom_start=6, control_scale=True)

# Define color scale
min_val = np.min(spi_data)
max_val = np.max(spi_data)
color_scale = folium.LinearColormap(
    colors=["red", "yellow", "green"],
    vmin=min_val,
    vmax=max_val,
    caption="SPI Values"
)
color_scale.add_to(m)

# Add SPI data to the map
folium.raster_layers.ImageOverlay(
    image=spi_data,
    bounds=[[src.bounds.bottom, src.bounds.left], [src.bounds.top, src.bounds.right]],
    colormap=lambda x: color_scale(x),
    opacity=0.6,
).add_to(m)

# Render the map in Streamlit
st_data = st_folium(m, width=800, height=600)


