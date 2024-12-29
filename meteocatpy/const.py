"""meteocatpy constants."""
BASE_URL = "https://api.meteo.cat"
MUNICIPIS_LIST_URL = "/referencia/v1/municipis"
MUNICIPIS_HORA_URL = "/pronostic/v1/municipalHoraria/{codi}"
MUNICIPIS_DIA_URL = "/pronostic/v1/municipal/{codi}"
SYMBOLS_URL = "/referencia/v1/simbols"
QUOTES_URL = "/quotes/v1/consum-actual"
STATIONS_LIST_URL = "/xema/v1/estacions/metadades"
INFO_STATION_URL = "/xema/v1/estacions/{codi_estacio}/metadades"
STATIONS_MUNICIPI_URL = "/xema/v1/representatives/metadades/municipis/{codi_municipi}/variables/{codi_variable}"
VARIABLES_URL = "/xema/v1/variables/mesurades/metadades"
STATION_DATA_URL = "/xema/v1/estacions/mesurades/{codiEstacio}/{any}/{mes}/{dia}"
UVI_DATA_URL = "/pronostic/v1/uvi/{codi_municipi}"
