# SPI Drought Monitoring Application

This is a Streamlit-based application for visualizing and analyzing SPI (Standardized Precipitation Index) data. The app uses GeoTIFF format for SPI data and Folium for map visualizations.

## Project Structure

- **SPI_12_2023.tif**: The raw SPI data in GeoTIFF format.
- **app.py**: The main application script that displays the map and visualizations.
- **requirements.txt**: Python dependencies required to run the app.


## Running the Application

To run the app locally, make sure you have Python installed. Then, install the required dependencies and start the Streamlit app:

```bash
pip install -r requirements.txt
streamlit run app.py



### 1. **`.gitignore`** (Git ignore file)

The `.gitignore` remains the same as before.



### 2. **`SPI_12_2023.tif`** (GeoTIFF file)

Make sure your `SPI_12_2023.tif` file is placed in the root of the project. This file will be read and processed in the `app.py` script.

---

With these updates, your app will now read the GeoTIFF file (`SPI_12_2023.tif`), convert it to GeoJSON, and display the data on a map using Folium. Let me know if you need further assistance or adjustments!

