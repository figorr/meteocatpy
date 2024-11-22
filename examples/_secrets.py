"""METEOCAT Secrets."""

from dotenv import load_dotenv
import os
from meteocatpy.interface import ConnectionOptions

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Ahora puedes acceder a la variable de entorno
METEOCAT_API_KEY = os.getenv("METEOCAT_API_KEY")

if METEOCAT_API_KEY is None:
    raise ValueError("La clave de API de Meteocat no está definida en el archivo .env")

METEOCAT_COORDS = (40.3049863, -3.7550013)
METEOCAT_DATA_DIR = "api-data"
METEOCAT_OPTIONS = ConnectionOptions(
    api_key= os.getenv("METEOCAT_API_KEY"),
    station_data=True,
)
METEOCAT_TOWN = "082956"
