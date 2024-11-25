import os
import pytest
import json
from dotenv import load_dotenv
from meteocatpy.stations import MeteocatStations

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"

@pytest.mark.asyncio
async def test_stations():
    # Crear una instancia de MeteocatStations con la API Key
    stations_client = MeteocatStations(API_KEY)

    # Obtener las estaciones
    stations_data = await stations_client.get_stations()

    # Crear la carpeta si no existe
    os.makedirs('tests/files', exist_ok=True)
    
    # Guardar los datos de las estaciones en un archivo JSON
    with open('tests/files/stations.json', 'w', encoding='utf-8') as f:
        json.dump(stations_data, f, ensure_ascii=False, indent=4)
    
    # Verificar que los municipios no estén vacíos
    assert stations_data, "Estaciones data is empty"