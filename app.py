import streamlit as st
import folium
import rasterio
from folium.raster_layers import ImageOverlay

# Streamlit app title
st.title("GeoTIFF with OpenStreetMap Overlay")

# Load your GeoTIFF file
tif_file = 'SPI_12_2023.tif'

# Read the GeoTIFF file using rasterio
with rasterio.open(tif_file) as src:
    img_data = src.read(1)  # Read image data (band 1)
    bounds = src.bounds  # Get bounds of the GeoTIFF

# Create a folium map centered around the bounds of your GeoTIFF
m = folium.Map(location=[(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2], zoom_start=10)

# Add OpenStreetMap as the base map (this is the default)
folium.TileLayer('OpenStreetMap').add_to(m)

# Add the GeoTIFF as an image overlay
ImageOverlay(
    image=img_data,
    bounds=[[bounds[1], bounds[0]], [bounds[3], bounds[2]]],  # bottom-left and top-right
    opacity=0.6,
).add_to(m)

# Save the map to an HTML file
map_html = 'map.html'
m.save(map_html)

# Display the map using Streamlit's HTML component
st.components.v1.html(open(map_html, 'r').read(), height=600, width=800)



