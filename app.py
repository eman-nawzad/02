import streamlit as st
import folium
import rasterio
from rasterio import features
import geopandas as gpd
from shapely.geometry import shape
import json
from folium import raster_layers
from io import BytesIO

# Function to read the GeoTIFF file and convert it to GeoJSON
def geotiff_to_geojson(tif_path):
    # Open the GeoTIFF file
    with rasterio.open(tif_path) as src:
        # Read the data and metadata
        image_data = src.read(1)
        transform = src.transform
        
        # Convert the raster to polygons (GeoJSON)
        mask = image_data != src.nodata
        shapes = features.shapes(image_data, mask=mask, transform=transform)
        
        # Convert shapes to GeoJSON format
        geojson = {"type": "FeatureCollection", "features": []}
        for shape, value in shapes:
            feature = {
                "type": "Feature",
                "geometry": shape.__geo_interface__,
                "properties": {"value": value},
            }
            geojson["features"].append(feature)
            
    return geojson

# Streamlit app layout
st.title("SPI Drought Monitoring Application")

st.markdown(
    """
    This is a Streamlit-based application for visualizing and analyzing SPI (Standardized Precipitation Index) data.
    The app uses a GeoTIFF file for SPI data and Folium for map visualizations.
    """
)

# File upload widget for the GeoTIFF file
tif_file = st.file_uploader("Upload the SPI GeoTIFF File", type=["tif", "tiff"])

if tif_file is not None:
    # Save the uploaded file temporarily
    with open("SPI_12_2023.tif", "wb") as f:
        f.write(tif_file.getbuffer())
    
    # Convert the uploaded GeoTIFF to GeoJSON
    geojson_data = geotiff_to_geojson("SPI_12_2023.tif")
    
    # Create a Folium map centered around the area
    folium_map = folium.Map(location=[0, 0], zoom_start=2, control_scale=True)
    
    # Add GeoJSON data to the map
    folium.GeoJson(geojson_data).add_to(folium_map)
    
    # Render the Folium map in Streamlit
    folium_map_html = folium_map._repr_html_()
    st.components.v1.html(folium_map_html, height=600)

    # Optionally, download the GeoJSON
    geojson_str = json.dumps(geojson_data)
    st.download_button(
        label="Download GeoJSON",
        data=geojson_str,
        file_name="SPI_12_2023.geojson",
        mime="application/geo+json",
    )

else:
    st.write("Please upload a GeoTIFF file to continue.")

