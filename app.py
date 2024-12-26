import streamlit as st
import folium
import geopandas as gpd
import rasterio
from rasterio.features import shapes
import json
from folium import plugins
from io import BytesIO

# Function to read GeoTIFF and convert to GeoJSON
def geotiff_to_geojson(tiff_file):
    with rasterio.open(tiff_file) as src:
        image = src.read(1)  # Read the first band
        mask = image != src.nodata
        results = shapes(image, mask=mask, transform=src.transform)
        
        geoms = []
        for geom, value in results:
            geoms.append({
                "type": "Feature",
                "geometry": geom,
                "properties": {"value": value}
            })
        
        return {"type": "FeatureCollection", "features": geoms}

# Title for the app
st.title("SPI Drought Monitoring")

# Path to the GeoTIFF file
tiff_file_path = 'SPI_12_2023.tif'

# Convert the GeoTIFF to GeoJSON
geojson_data = geotiff_to_geojson(tiff_file_path)

# Create a map centered around a specific location
m = folium.Map(location=[35.5, 44.3], zoom_start=10)

# Add the GeoJSON to the map
folium.GeoJson(geojson_data).add_to(m)

# Display the map in Streamlit
from streamlit_folium import folium_static
folium_static(m)

