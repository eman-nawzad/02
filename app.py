import streamlit as st
import geopandas as gpd
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import numpy as np

# App title
st.title("Drought Monitoring Web Application")

# Sidebar for user input
st.sidebar.header("Data Upload")
spi_file = "SPI_12_2023.tif"  # SPI GeoTIFF file
shapefile_option = st.sidebar.checkbox("Overlay vector data (GeoJSON/Shapefile)")

# Load SPI GeoTIFF data
@st.cache_data
def load_spi_data(file):
    with rasterio.open(file) as src:
        data = src.read(1)  # Read the first band
        profile = src.profile
    return data, profile

# Categorize drought thresholds
def categorize_drought(data):
    categories = np.empty_like(data, dtype=object)
    categories[data < -2.00] = "Extreme drought"
    categories[(data >= -1.99) & (data <= -1.50)] = "Severe drought"
    categories[(data >= -1.49) & (data <= -1.00)] = "Moderate drought"
    categories[(data >= -0.99) & (data <= 0.00)] = "Mild drought"
    return categories

# Load GeoJSON or Shapefile
@st.cache_data
def load_vector_data(vector_file):
    return gpd.read_file(vector_file)

# Display SPI data
spi_data, profile = load_spi_data(spi_file)
st.sidebar.write("SPI Data Loaded Successfully!")

# Plot SPI data
fig, ax = plt.subplots(figsize=(10, 6))
show(spi_data, ax=ax, title="SPI Drought Map", cmap="coolwarm")

# Overlay vector data if enabled
if shapefile_option:
    uploaded_vector_file = st.sidebar.file_uploader("Upload GeoJSON/Shapefile", type=["geojson", "shp", "zip"])
    if uploaded_vector_file:
        vector_data = load_vector_data(uploaded_vector_file)
        vector_data.plot(ax=ax, edgecolor="black", facecolor="none")
        st.sidebar.write("Vector data overlaid!")

# Show the plot
st.pyplot(fig)

# Categorize drought and display
st.header("Drought Categories")
categories = categorize_drought(spi_data)

# Add legend
legend = """
- **Extreme drought**: Less than -2.00  
- **Severe drought**: -1.50 to -1.99  
- **Moderate drought**: -1.00 to -1.49  
- **Mild drought**: -0.99 to -0.00  
"""
st.markdown(legend)

# Additional notes
st.sidebar.info(
    """
    - Ensure your GeoJSON/Shapefile matches the coordinate reference system (CRS) of the raster file.
    - The SPI map is visualized in `coolwarm` color mapping.
    """
)





