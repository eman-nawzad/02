import folium
import rasterio
from folium import raster_layers
import numpy as np

# Open your GeoTIFF file
with rasterio.open('your_geotiff_file.tif') as src:
    # Get the bounding box of the raster
    bounds = src.bounds
    # Read the raster data
    image = src.read(1)  # You can change this if your raster has multiple bands

# Create a folium map centered around the bounding box of the raster
m = folium.Map(location=[(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2], zoom_start=12)

# Add OpenStreetMap as a basemap
folium.TileLayer('OpenStreetMap').add_to(m)

# Convert the raster data to a format that folium can display
raster_layer = raster_layers.ImageOverlay(
    image, 
    bounds=[[bounds[1], bounds[0]], [bounds[3], bounds[2]]],
    opacity=0.5
)

# Add the raster layer to the map
raster_layer.add_to(m)

# Save the map to an HTML file or display
m.save('map_with_raster_and_osm.html')


# Save the map to an HTML file or display
m.save('map_with_raster_and_osm.html')




