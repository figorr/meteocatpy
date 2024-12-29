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

    try:
        # Obtener los datos de las alertas
        alerts_data = await alerts_client.get_alerts()
    except Exception as e:
        pytest.fail(f"Failed to fetch alerts: {e}")

    # Crear la carpeta si no existe
    os.makedirs('tests/files', exist_ok=True)

    # Guardar los datos de las alertas en un archivo JSON
    with open('tests/files/alerts.json', 'w', encoding='utf-8') as f:
        json.dump(alerts_data, f, ensure_ascii=False, indent=4)

    # Validar la respuesta
    assert isinstance(alerts_data, list), "Alerts data should be a list"
    if not alerts_data:
        # Mensaje indicando que no hay alertas activas
        print("No active alerts.")
        assert alerts_data == [], "No active alerts."
