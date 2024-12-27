import streamlit as st
import folium
import rasterio
from rasterio import features
import geopandas as gpd
from shapely.geometry import shape
import json
from io import BytesIO

# Function to read the GeoTIFF file and convert it to GeoJSON
def geotiff_to_geojson(file_obj):
    with rasterio.open(file_obj) as src:
        image_data = src.read(1)
        transform = src.transform
        nodata_value = src.nodata if src.nodata is not None else 0
        mask = image_data != nodata_value
        shapes = features.shapes(image_data, mask=mask, transform=transform)

        geojson = {"type": "FeatureCollection", "features": []}
        for geom, value in shapes:
            feature = {
                "type": "Feature",
                "geometry": shape(geom).__geo_interface__,
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
    tif_file_buffer = BytesIO(tif_file.read())
    
    # Convert the uploaded GeoTIFF to GeoJSON
    geojson_data = geotiff_to_geojson(tif_file_buffer)
    
    # Open the GeoTIFF file to determine the map center
    with rasterio.open(tif_file_buffer) as src:
        bounds = src.bounds
        center = [(bounds.top + bounds.bottom) / 2, (bounds.left + bounds.right) / 2]
    
    # Create a Folium map centered around the area
    folium_map = folium.Map(location=center, zoom_start=10, control_scale=True)
    
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


