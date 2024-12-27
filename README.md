# Drought Monitoring App

This repository contains a Streamlit web application for monitoring drought using the Standardized Precipitation Index (SPI) dataset.

## Features

- Displays the SPI map for a 12-month period (2023) based on the provided GeoTIFF file.
- Calculates and displays statistical information about the SPI values (minimum, maximum, and mean).
- Interactive visualization with a custom colormap to indicate drought and wetness levels.

## Repository Structure

```
.gitignore
README.md
SPI_12_2023.tif
app.py
requirements.txt
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. Open the application in your web browser at `http://localhost:8501`.

## Dependencies

- Python 3.x
- Streamlit
- Rasterio
- Matplotlib
- NumPy

## Usage

Ensure the `SPI_12_2023.tif` file is placed in the root of the repository. Run the application to visualize the SPI map and analyze drought conditions for the specified period.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

Developed by [eman nawzad].


