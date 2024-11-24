import os
import pytest
import json
from dotenv import load_dotenv
from meteocatpy.symbols import MeteocatSymbols

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"

@pytest.mark.asyncio
async def test_simbols():
    # Crear una instancia de MeteocatSymbols con la API Key
    symbols_client = MeteocatSymbols(API_KEY)

    # Obtener los símbolos
    simbolos_data = await symbols_client.get_simbols()
    
    # Guardar los datos de los símbolos en un archivo JSON
    with open('tests/files/simbols.json', 'w', encoding='utf-8') as f:
        json.dump(simbolos_data, f, ensure_ascii=False, indent=4)
    
    # Verificar que los símbolos no estén vacíos
    assert simbolos_data, "Simbols data is empty"