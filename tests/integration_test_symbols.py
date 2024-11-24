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
    simbolos_data = await symbols_client.fetch_symbols()

    # Verificar la estructura de los datos obtenidos
    print("Estructura de los datos obtenidos:")
    print(simbolos_data)  # Esto te mostrará si realmente es una lista de categorías

    # Crear la carpeta si no existe
    os.makedirs('tests/files', exist_ok=True)
    
    # Guardar el JSON completo original
    with open('tests/files/simbols.json', 'w', encoding='utf-8') as f:
        json.dump(simbolos_data, f, ensure_ascii=False, indent=4)

    # Verificar que los símbolos no estén vacíos
    assert simbolos_data, "Simbols data is empty"
    
    # Iterar sobre las categorías y guardar cada una en su propio archivo
    for category in simbolos_data:
        if "valors" in category:  # Asegurarse de que tenga "valors"
            category_name = category['nom']  # Nombre de la categoría (e.g., "cel", "mar", etc.)
            
            # Reemplazar los espacios por guiones bajos en el nombre de la categoría
            category_name_safe = category_name.replace(' ', '_')
            
            # Nombre del archivo con el prefijo "simbols_"
            category_file_name = f'tests/files/simbols_{category_name_safe}.json'
            
            # Guardar la categoría y sus valores en un archivo JSON
            category_data = {
                "nom": category_name,
                "descripcio": category["descripcio"],
                "valors": category["valors"]
            }

            with open(category_file_name, 'w', encoding='utf-8') as f:
                json.dump(category_data, f, ensure_ascii=False, indent=4)
    
    # Asegurarse de que se hayan creado los archivos correctamente
    for category in simbolos_data:
        if "valors" in category:
            category_name = category['nom']
            
            # Reemplazar los espacios por guiones bajos también al verificar
            category_name_safe = category_name.replace(' ', '_')
            
            category_file_name = f'tests/files/simbols_{category_name_safe}.json'
            assert os.path.exists(category_file_name), f"File for category {category_name} was not created"
