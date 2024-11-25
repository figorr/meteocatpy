import os
import pytest
import json
from dotenv import load_dotenv
from meteocatpy.variables import MeteocatVariables

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"

@pytest.mark.asyncio
async def test_variables():
    # Crear una instancia de MeteocatVariables con la API Key
    variables_client = MeteocatVariables(API_KEY)

    # Obtener las variables
    variables_data = await variables_client.get_variables()

    # Crear la carpeta si no existe
    os.makedirs('tests/files', exist_ok=True)
    
    # Guardar los datos de las variables en un archivo JSON
    with open('tests/files/variables.json', 'w', encoding='utf-8') as f:
        json.dump(variables_data, f, ensure_ascii=False, indent=4)
    
    # Verificar que las variables no estén vacías
    assert variables_data, "Variables data is empty"
