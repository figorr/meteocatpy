import os
import pytest
import json
from dotenv import load_dotenv
from meteocatpy.quotes import MeteocatQuotes

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"

@pytest.mark.asyncio
async def test_quotes():
    # Crear una instancia de MeteocatTown con la API Key
    quotes_client = MeteocatQuotes(API_KEY)

    # Obtener los municipios
    quotes_data = await quotes_client.get_quotes()

    # Crear la carpeta si no existe
    os.makedirs('tests/files', exist_ok=True)
    
    # Guardar los datos de los municipios en un archivo JSON
    with open('tests/files/quotes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes_data, f, ensure_ascii=False, indent=4)
    
    # Verificar que los municipios no estén vacíos
    assert quotes_data, "Quotes data is empty"