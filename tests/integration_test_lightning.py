import os
import pytest
import json
from dotenv import load_dotenv
from meteocatpy.lightning import MeteocatLightningData

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY_TEST")
REGION_CODI_TEST = os.getenv("REGION_CODI_TEST")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"
assert REGION_CODI_TEST, "Region codi test is required"

@pytest.mark.asyncio
async def test_lightning():
    # Crear una instancia de MeteocatLightningData con la API Key
    lightning_client = MeteocatLightningData(API_KEY)

    # Obtener los datos de rayos
    lightning_data = await lightning_client.get_lightning_data(REGION_CODI_TEST)

    print("Datos de la API:", lightning_data)  # Para depuración

    # Crear la carpeta si no existe
    os.makedirs('tests/files', exist_ok=True)
    
    # Guardar los datos de rayos en un archivo JSON
    with open(f'tests/files/lightning_{REGION_CODI_TEST}_data.json', 'w', encoding='utf-8') as f:
        json.dump(lightning_data, f, ensure_ascii=False, indent=4)
    
    # Verificar que los datos de rayos sean una lista
    assert isinstance(lightning_data, list), "La respuesta no es una lista"