import aiohttp
from .const import BASE_URL, MUNICIPIS_LIST_URL, MUNICIPIS_HORA_URL, MUNICIPIS_DIA_URL


class MeteocatClient:
    """Cliente para interactuar con la API de Meteocat."""

    def __init__(self, api_key: str):
        """
        Inicializa el cliente Meteocat.
        
        Args:
            api_key (str): Clave de API para autenticar las solicitudes.
        """
        self.api_key = api_key
        self.headers = {"X-Api-Key": self.api_key}

    async def get_municipis(self):
        """
        Obtiene la lista de municipios desde la API de Meteocat.

        Returns:
            dict: Datos de los municipios.
        """
        url = f"{BASE_URL}{MUNICIPIS_LIST_URL}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status != 200:
                    raise Exception(f"Error {response.status}: {await response.text()}")
                return await response.json()

    async def get_prediccion_horaria(self, codi: str):
        """
        Obtiene la predicción horaria a 72 horas para un municipio.

        Args:
            codi (str): Código del municipio.

        Returns:
            dict: Predicción horaria para el municipio.
        """
        url = f"{BASE_URL}{MUNICIPIS_HORA_URL.format(codi=codi)}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status != 200:
                    raise Exception(f"Error {response.status}: {await response.text()}")
                return await response.json()

    async def get_prediccion_diaria(self, codi: str):
        """
        Obtiene la predicción diaria a 8 días para un municipio.

        Args:
            codi (str): Código del municipio.

        Returns:
            dict: Predicción diaria para el municipio.
        """
        url = f"{BASE_URL}{MUNICIPIS_DIA_URL.format(codi=codi)}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status != 200:
                    raise Exception(f"Error {response.status}: {await response.text()}")
                return await response.json()
