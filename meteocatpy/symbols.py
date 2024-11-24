import aiohttp
from .const import BASE_URL, SYMBOLS_URL
from .exceptions import BadRequestError, ForbiddenError, TooManyRequestsError, InternalServerError, UnknownAPIError


class MeteocatSymbols:
    """Clase para interactuar con la API de símbolos de Meteocat."""

    def __init__(self, api_key: str):
        """
        Inicializa la clase MeteocatSymbols.

        Args:
            api_key (str): Clave de API para autenticar las solicitudes.
        """
        self.api_key = api_key
        self.headers = {"X-Api-Key": self.api_key}
        self.symbols_map = {}

    async def fetch_symbols(self):
        """
        Descarga los datos de símbolos desde la API de Meteocat y los guarda en un diccionario.

        Returns:
            dict: Mapeo de códigos de símbolo a sus descripciones.
        """
        url = f"{BASE_URL}{SYMBOLS_URL}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Convertimos los datos a un diccionario accesible
                        self.symbols_map = {int(item["codi"]): item["nom"] for item in data["valors"]}
                        return self.symbols_map

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
                raise UnknownAPIError(f"Error al conectar con la API de Meteocat: {str(e)}")

            except Exception as ex:
                raise UnknownAPIError(f"Error inesperado: {str(ex)}")

    def get_description(self, code: int) -> str:
        """
        Obtiene la descripción de un código de símbolo.

        Args:
            code (int): Código del símbolo.

        Returns:
            str: Descripción del símbolo. Retorna 'Desconocido' si el código no está en el mapeo.
        """
        return self.symbols_map.get(code, "Desconocido")
