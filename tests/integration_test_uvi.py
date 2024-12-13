import os
import pytest
import json
from dotenv import load_dotenv
from meteocatpy.uvi import MeteocatUviData

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY")
MUNICIPI_CODI_TEST = os.getenv("MUNICIPI_CODI_TEST")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"
assert MUNICIPI_CODI_TEST, "Station codi test is required"

@pytest.mark.asyncio
async def test_municipis():
    # Crear una instancia de MeteocatUviData con la API Key
    uvi_client = MeteocatUviData(API_KEY)

    # Obtener los datos del índice UVI
    uvi_data = await uvi_client.get_uvi_index(MUNICIPI_CODI_TEST)

    # Crear la carpeta si no existe
    os.makedirs('tests/files', exist_ok=True)
    
    # Guardar los datos del índice UVI en un archivo JSON
    with open(f'tests/files/uvi_index_{MUNICIPI_CODI_TEST}.json', 'w', encoding='utf-8') as f:
        json.dump(uvi_data, f, ensure_ascii=False, indent=4)
    
    # Verificar que los datos del índice UVI no estén vacíos
    assert uvi_data, "UVI data is empty"