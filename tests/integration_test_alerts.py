import os
import pytest
import json
from dotenv import load_dotenv
from meteocatpy.alerts import MeteocatAlerts

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"

@pytest.mark.asyncio
async def test_alerts():
    # Crear una instancia de MeteocatAlerts con la API Key
    alerts_client = MeteocatAlerts(API_KEY)

    # Obtener los datos de las alertas
    alerts_data = await alerts_client.get_alerts()

    # Crear la carpeta si no existe
    os.makedirs('tests/files', exist_ok=True)
    
    # Guardar los datos de las alertas en un archivo JSON
    with open(f'tests/files/alerts.json', 'w', encoding='utf-8') as f:
        json.dump(alerts_data, f, ensure_ascii=False, indent=4)
    
    # Verificar que los datos no estén vacíos
    assert alerts_data, "Alerts data is empty"