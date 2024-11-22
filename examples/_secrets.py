"""METEOCAT Secrets."""

from meteocatpy.interface import ConnectionOptions

METEOCAT_COORDS = (40.3049863, -3.7550013)
METEOCAT_DATA_DIR = "api-data"
METEOCAT_OPTIONS = ConnectionOptions(
    api_key="MY_API_KEY",
    station_data=True,
)
METEOCAT_TOWN = "082956"