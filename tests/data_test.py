import os
import pytest
from aioresponses import aioresponses
from meteocatpy.data import MeteocatStationData
from meteocatpy.exceptions import (
    BadRequestError,
    ForbiddenError,
    TooManyRequestsError,
    InternalServerError,
    UnknownAPIError,
)
from meteocatpy.const import BASE_URL, STATION_DATA_URL
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener los valores del archivo .env
API_KEY = os.getenv("METEOCAT_API_KEY")
STATION_CODI_TEST = os.getenv("STATION_CODI_TEST")

# Asegúrate de que las variables estén definidas
assert API_KEY, "API Key is required"
assert STATION_CODI_TEST, "Station codi test is required"

@pytest.mark.asyncio
async def test_get_station_data():
    # Simular la respuesta de la API
    test_url = f"{BASE_URL}{STATION_DATA_URL}".format(
        codiEstacio=STATION_CODI_TEST, any=2024, mes="12", dia="04"
    )
    mock_response = {
        "lectures": [
            {"codi_variable": 32, "data": "2024-12-04T12:00:00Z", "valor": 15.2},
            {"codi_variable": 33, "data": "2024-12-04T12:00:00Z", "valor": 80},
        ]
    }

    with aioresponses() as mock:
        mock.get(test_url, payload=mock_response)

        station_data = MeteocatStationData(API_KEY)
        result = await station_data.get_station_data(STATION_CODI_TEST)

        assert result == mock_response


@pytest.mark.asyncio
async def test_get_station_data_with_variables(mocker):
    # Simular la respuesta de la API y las variables
    test_url = f"{BASE_URL}{STATION_DATA_URL}".format(
        codiEstacio=STATION_CODI_TEST, any=2024, mes="12", dia="04"
    )
    mock_station_response = {
        "lectures": [
            {"codi_variable": 32, "data": "2024-12-04T12:00:00Z", "valor": 15.2},
            {"codi_variable": 33, "data": "2024-12-04T12:00:00Z", "valor": 80},
        ]
    }
    mock_variables_response = [
        {"codi": 32, "nom": "Temperatura"},
        {"codi": 33, "nom": "Humedad relativa"},
    ]

    # Mockear la llamada a la API y las variables
    with aioresponses() as mock:
        mock.get(test_url, payload=mock_station_response)
        mocker.patch(
            "meteocatpy.data.MeteocatVariables.get_variables",
            return_value=mock_variables_response,
        )

        station_data = MeteocatStationData(API_KEY)
        result = await station_data.get_station_data_with_variables(STATION_CODI_TEST)

        # Validar los datos organizados por variables
        expected_result = {
            "Temperatura": [
                {
                    "data": "2024-12-04T12:00:00Z",
                    "valor": 15.2,
                    "estat": "",
                    "base_horaria": "",
                }
            ],
            "Humedad relativa": [
                {
                    "data": "2024-12-04T12:00:00Z",
                    "valor": 80,
                    "estat": "",
                    "base_horaria": "",
                }
            ],
        }
        assert result == expected_result


@pytest.mark.asyncio
async def test_get_station_data_errors():
    test_url = f"{BASE_URL}{STATION_DATA_URL}".format(
        codiEstacio=STATION_CODI_TEST, any=2024, mes="12", dia="04"
    )

    # Simular errores de la API
    with aioresponses() as mock:
        mock.get(test_url, status=400, payload={"message": "Bad Request"})
        station_data = MeteocatStationData(API_KEY)

        with pytest.raises(BadRequestError):
            await station_data.get_station_data(STATION_CODI_TEST)

        mock.get(test_url, status=403, payload={"message": "Forbidden"})
        with pytest.raises(ForbiddenError):
            await station_data.get_station_data(STATION_CODI_TEST)

        mock.get(test_url, status=429, payload={"message": "Too Many Requests"})
        with pytest.raises(TooManyRequestsError):
            await station_data.get_station_data(STATION_CODI_TEST)

        mock.get(test_url, status=500, payload={"message": "Internal Server Error"})
        with pytest.raises(InternalServerError):
            await station_data.get_station_data(STATION_CODI_TEST)
