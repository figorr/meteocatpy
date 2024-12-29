import os
import pytest
import json
from dotenv import load_dotenv
from meteocatpy.infostation import MeteocatInfoStation

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY")
STATION_CODI_TEST = os.getenv("STATION_CODI_TEST")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"
assert STATION_CODI_TEST, "Station codi test is required"

@pytest.mark.asyncio
async def test_infostation():
    # Crear una instancia de MeteocatInfoStation con la API Key
    infostation_client = MeteocatInfoStation(API_KEY)

    # Obtener los datos de la estación
    station_data = await infostation_client.get_infostation(STATION_CODI_TEST)

    # Crear la carpeta si no existe
    os.makedirs('tests/files', exist_ok=True)
    
    # Guardar los datos de las estaciones en un archivo JSON
    with open(f'tests/files/station_{STATION_CODI_TEST}_info.json', 'w', encoding='utf-8') as f:
        json.dump(station_data, f, ensure_ascii=False, indent=4)
    
    # Verificar que los datos no estén vacíos
    assert station_data, "Estaciones info is empty"