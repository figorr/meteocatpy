import aiohttp

from .helpers import extract_available_date, session_context
import logging
from datetime import datetime, timezone
from .const import BASE_URL, ALERTS_URL
from .exceptions import (
    BadRequestError,
    ForbiddenError,
    TooManyRequestsError,
    InternalServerError,
    UnknownAPIError,
)

_LOGGER = logging.getLogger(__name__)

class MeteocatAlerts:
    """Clase para interactuar con los datos de estaciones de la API de Meteocat."""

    def __init__(
        self,
        api_key: str,
        session: aiohttp.ClientSession | None = None,
    ):
        """
        Inicializa la clase MeteocatAlerts.

        Args:
            api_key (str): Clave de API para autenticar las solicitudes.
        """
        self.api_key = api_key
        self._session = session
        self.headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key,
        }
    
    @staticmethod
    def get_current_date():
        """
        Obtiene la fecha actual en formato numérico.

        Returns:
            tuple: Año (YYYY), mes (MM), día (DD) como enteros.
        """
        now = datetime.now(timezone.utc)
        return now.year, now.month, now.day

    async def get_alerts(self):
        """
        Obtiene los datos meteorológicos de alertas desde la API de Meteocat.

        Args:
            any (str): Año de la consulta.
            mes (str): Mes de la consulta.
            dia (str): Día de la consulta.

        Returns:
            dict: Datos de alertas meteorológicas.
        """
        any, mes, dia = self.get_current_date()  # Calcula la fecha actual
        url = f"{BASE_URL}{ALERTS_URL}".format(
            any=any, mes=f"{mes:02d}", dia=f"{dia:02d}"
        )
    
        async with session_context(self._session) as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()

                    # Gestionar errores según el código de estado
                    if response.status == 400:
                        error_data = await response.json()
                        # Reintentar con la fecha válida más reciente del mensaje
                        available_date = extract_available_date(
                            error_data.get("message")
                        )
                        if available_date:
                            new_url = f"{BASE_URL}{ALERTS_URL}".format(
                                any=available_date.year,
                                mes=f"{available_date.month:02d}",
                                dia=f"{available_date.day:02d}",
                            )
                            async with session.get(new_url, headers=self.headers) as new_response:
                                if new_response.status == 200:
                                    return await new_response.json()
                                raise UnknownAPIError(
                                    f"Failed with the valid date {available_date}: {await new_response.text()}"
                                )
                        raise BadRequestError(error_data)
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
                raise UnknownAPIError(
                    message=f"Error al conectar con la API de Meteocat: {str(e)}",
                    status_code=0,
                )

            except Exception as ex:
                raise UnknownAPIError(
                    message=f"Error inesperado: {str(ex)}",
                    status_code=0,
                )
