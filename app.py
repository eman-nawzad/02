import folium
import rasterio
from folium.raster_layers import ImageOverlay
from flask import Flask, render_template

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    # Load your GeoTIFF file
    tif_file = 'SPI_12_2023.tif'
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
    map_html = 'templates/map.html'  # Ensure the map is saved in a template folder
    m.save(map_html)

    return render_template('map.html')  # Render the saved map HTML

if __name__ == '__main__':
    app.run(debug=True)



