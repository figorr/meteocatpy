import pytest
import aiohttp
from unittest.mock import patch, AsyncMock
from meteocatpy.client import MeteocatClient

@pytest.mark.asyncio
async def test_get_municipis():
    """Test que asegura que el método get_municipis funcione correctamente."""

    # Simulamos una respuesta exitosa de la API
    mock_response = {"municipis": [{"nom": "Barcelona", "codi": 1}]}

    # Creamos el cliente con una clave API ficticia
    client = MeteocatClient("api_test_key")

    # Usamos patch para simular el comportamiento de aiohttp.ClientSession
    with patch.object(aiohttp.ClientSession, "get", return_value=AsyncMock(
        __aenter__=AsyncMock(return_value=AsyncMock(
            status=200,
            json=AsyncMock(return_value=mock_response),
            text=AsyncMock(return_value="{}")  # Mock de la respuesta de text()
        ))
    )):

        municipis = await client.get_municipis()
        assert municipis == mock_response