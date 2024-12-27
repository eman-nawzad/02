import streamlit as st
import rasterio
import folium
from streamlit_folium import st_folium
import numpy as np

st.title("SPI Drought Map")

# Load the SPI GeoTIFF file
file_path = "SPI_12_2023.tif"
with rasterio.open(file_path) as src:
    spi_data = src.read(1)
    bounds = [
        [src.bounds.bottom, src.bounds.left],
        [src.bounds.top, src.bounds.right]
    ]

# Create the map
m = folium.Map(location=[35, 44], zoom_start=6)

# Add SPI data as an image overlay
folium.raster_layers.ImageOverlay(
    image=spi_data,
    bounds=bounds,
    opacity=0.6,
).add_to(m)

# Render the map in Streamlit
st_folium(m, width=800, height=600)



