import os
import pytest
import json
from dotenv import load_dotenv
from meteocatpy.data import MeteocatStationData

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY")
STATION_CODI_TEST = os.getenv("STATION_CODI_TEST")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"
assert STATION_CODI_TEST, "Station codi test is required"

@pytest.mark.asyncio
async def test_stations_data():
    # Crear una instancia de MeteocatStationData con la API Key
    data_client = MeteocatStationData(API_KEY)

    # Obtener los datos de la estación
    station_data = await data_client.get_station_data(STATION_CODI_TEST)

    # Crear la carpeta si no existe
    os.makedirs('tests/files', exist_ok=True)
    
    # Guardar los datos de las estaciones en un archivo JSON
    with open('tests/files/station_data.json', 'w', encoding='utf-8') as f:
        json.dump(station_data, f, ensure_ascii=False, indent=4)
    
    # Verificar que los datos no estén vacíos
    assert station_data, "Estaciones data is empty"