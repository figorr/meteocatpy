import aiohttp
from datetime import datetime
from .const import BASE_URL, STATION_DATA_URL
from .exceptions import BadRequestError, ForbiddenError, TooManyRequestsError, InternalServerError, UnknownAPIError

class MeteocatStationData:
    """Clase para interactuar con los datos de la estación en la API de Meteocat."""

    def __init__(self, api_key: str):
        """
        Inicializa la clase MeteocatStationData.

        Args:
            api_key (str): Clave de API para autenticar las solicitudes.
        """
        self.api_key = api_key
        self.headers = {"X-Api-Key": self.api_key}

    @staticmethod
    def get_current_date():
        """
        Obtiene la fecha actual en formato numérico.

        Returns:
            tuple: Año (YYYY), mes (MM), día (DD) como enteros.
        """
        now = datetime.now()
        return now.year, now.month, now.day

    async def get_station_data(self, codiEstacio: str):
        """
        Obtiene los datos meteorológicos para el código de estación y fecha actual.

        Args:
            codiEstacio (str): Código de la estación.

        Returns:
            dict: Datos meteorológicos de la estación para la fecha actual.
        """
        any, mes, dia = self.get_current_date()  # Calcula la fecha actual
        url = f"{BASE_URL}{STATION_DATA_URL}".format(
            codiEstacio=codiEstacio, any=any, mes=f"{mes:02d}", dia=f"{dia:02d}"
        )

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()

                    # Gestionar errores según el código de estado
                    if response.status == 400:
                        raise BadRequestError(await response.json())
                    elif response.status == 403:
                        error_data = await response.json()
                        if error_data.get("message") == "Forbidden":
                            raise ForbiddenError(error_data)
                        elif error_data.get("message") == "Missing Authentication Token":
                            raise ForbiddenError(error_data)
                    elif response.status == 429:
                        raise TooManyRequestsError(await response.json())
                    elif response.status == 500:
                        raise InternalServerError(await response.json())
                    else:
                        raise UnknownAPIError(f"Unexpected error {response.status}: {await response.text()}")

            except aiohttp.ClientError as e:
                raise UnknownAPIError(
                    message=f"Error al conectar con la API de Meteocat: {str(e)}",
                    status_code=0,
                )

            except Exception as ex:
                raise UnknownAPIError(
                    message=f"Error inesperado: {str(ex)}",
                    status_code=0,
                )