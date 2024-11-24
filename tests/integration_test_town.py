import os
import pytest
import json
from dotenv import load_dotenv
from meteocatpy.town import MeteocatTown

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"

@pytest.mark.asyncio
async def test_municipis():
    # Crear una instancia de MeteocatTown con la API Key
    town_client = MeteocatTown(API_KEY)

    # Obtener los municipios
    municipios_data = await town_client.get_municipis()

    # Crear la carpeta si no existe
    os.makedirs('tests/files', exist_ok=True)
    
    # Guardar los datos de los municipios en un archivo JSON
    with open('tests/files/municipis.json', 'w', encoding='utf-8') as f:
        json.dump(municipios_data, f, ensure_ascii=False, indent=4)
    
    # Verificar que los municipios no estén vacíos
    assert municipios_data, "Municipis data is empty"
