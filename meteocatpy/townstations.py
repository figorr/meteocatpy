import aiohttp
from .const import BASE_URL, STATIONS_MUNICIPI_URL
from .exceptions import (
    BadRequestError,
    ForbiddenError,
    TooManyRequestsError,
    InternalServerError,
    UnknownAPIError
)

class MeteocatTownStations:
    """
    Clase para interactuar con la API de Meteocat y obtener
    las estaciones representativas de un municipio para una variable específica.
    """

    def __init__(self, api_key: str):
        """
        Inicializa la clase MeteocatTownStations.

        Args:
            api_key (str): Clave de API para autenticar las solicitudes.
        """
        self.api_key = api_key
        self.headers = {"X-Api-Key": self.api_key}

    async def get_town_stations(self, codi_municipi: str, codi_variable: str):
        """
        Obtiene la lista de estaciones representativas para un municipio y una variable específica.

        Args:
            codi_municipi (str): Código del municipio.
            codi_variable (str): Código de la variable.

        Returns:
            dict: Datos de las estaciones representativas.
        """
        url = f"{BASE_URL}{STATIONS_MUNICIPI_URL}".format(
            codi_municipi=codi_municipi, codi_variable=codi_variable
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
                        raise UnknownAPIError(
                            f"Unexpected error {response.status}: {await response.text()}"
                        )

            except aiohttp.ClientError as e:
                raise UnknownAPIError(f"Error al conectar con la API de Meteocat: {str(e)}")

            except Exception as ex:
                raise UnknownAPIError(f"Error inesperado: {str(ex)}")
