import os
import pytest
import json
from dotenv import load_dotenv
from meteocatpy.townstations import MeteocatTownStations

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY")
MUNICIPI_CODI_TEST = os.getenv("MUNICIPI_CODI_TEST")
VARIABLE_CODI_TEST = os.getenv("VARIABLE_CODI_TEST")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"
assert MUNICIPI_CODI_TEST, "Municipi codi test is required"
assert VARIABLE_CODI_TEST, "Variable codi test is required"

@pytest.mark.asyncio
async def test_town_stations():
    # Crear una instancia de MeteocatTownStations con la API Key
    town_stations_client = MeteocatTownStations(API_KEY)

    # Obtener la lista de estaciones del municipio usando el código de municipio de prueba y la variable de prueba
    town_stations_data = await town_stations_client.get_town_stations(MUNICIPI_CODI_TEST, VARIABLE_CODI_TEST)

    # Crear la carpeta si no existe
    os.makedirs('tests/files', exist_ok=True)
    
    # Guardar la lista de estaciones del municipio en un archivo JSON
    with open(f'tests/files/stations_{MUNICIPI_CODI_TEST}_{VARIABLE_CODI_TEST}.json', 'w', encoding='utf-8') as f:
        json.dump(town_stations_data, f, ensure_ascii=False, indent=4)
    
    # Verificar que la lista de estaciones del municipio no esté vacía
    assert town_stations_data, "Estaciones data is empty"
