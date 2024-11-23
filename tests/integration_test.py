import os
import pytest
from dotenv import load_dotenv
from meteocatpy.client import MeteocatClient

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY")
MUNICIPI_TEST = os.getenv("MUNICIPI_TEST")
MUNICIPI_CODI_TEST = os.getenv("MUNICIPI_CODI_TEST")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"
assert MUNICIPI_TEST, "Municipi test is required"
assert MUNICIPI_CODI_TEST, "Municipi codi test is required"

@pytest.mark.asyncio
async def test_municipis():
    # Crear una instancia de MeteocatClient con la API Key
    client = MeteocatClient(API_KEY)

    # Obtener los municipios
    municipios_data = await client.get_municipis()
    
    # Guardar los datos de los municipios en un archivo txt
    with open('tests/files/municipis.txt', 'w', encoding='utf-8') as f:
        f.write(str(municipios_data))
    
    # Verificar que los municipios no estén vacíos
    assert municipios_data, "Municipis data is empty"
    
    # Verificar que el municipio de prueba esté en la lista
    municipi_names = [m['nom'] for m in municipios_data]
    assert MUNICIPI_TEST in municipi_names, f"{MUNICIPI_TEST} not found in municipis list"

@pytest.mark.asyncio
async def test_predict_hora():
    # Crear una instancia de MeteocatClient con la API Key
    client = MeteocatClient(API_KEY)

    # Obtener la predicción horaria para el municipio de prueba
    prediccion_hora = await client.get_prediccion_hora(MUNICIPI_CODI_TEST)
    
    # Guardar la predicción horaria en un archivo txt
    with open('tests/files/predict_hora.txt', 'w', encoding='utf-8') as f:
        f.write(str(prediccion_hora))
    
    # Verificar que la predicción horaria no esté vacía
    assert prediccion_hora, "Prediccion horaria is empty"

@pytest.mark.asyncio
async def test_predict_dia():
    # Crear una instancia de MeteocatClient con la API Key
    client = MeteocatClient(API_KEY)

    # Obtener la predicción diaria para el municipio de prueba
    prediccion_dia = await client.get_prediccion_dia(MUNICIPI_CODI_TEST)
    
    # Guardar la predicción diaria en un archivo txt
    with open('tests/files/predict_dia.txt', 'w', encoding='utf-8') as f:
        f.write(str(prediccion_dia))
    
    # Verificar que la predicción diaria no esté vacía
    assert prediccion_dia, "Prediccion diaria is empty"
