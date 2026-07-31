import asyncio
import json
import os

from dotenv import load_dotenv
from meteocatpy.eto import MeteocatETO


async def main():
    load_dotenv()

    api_key = os.getenv("METEOCAT_API_KEY_TEST")
    station_id = os.getenv("STATION_CODI_TEST")

    if not api_key:
        raise ValueError("METEOCAT_API_KEY_TEST no está definido")

    if not station_id:
        raise ValueError("STATION_CODI_TEST no está definido")

    client = MeteocatETO(api_key)

    print(f"Solicitando datos ETo para la estación {station_id}...")

    try:
        eto_data = await client.get_eto_data(station_id)
    except Exception as err:
        print(f"Error: {err}")
        raise

    os.makedirs("tests/files", exist_ok=True)

    output = f"tests/files/eto_{station_id}.json"

    with open(output, "w", encoding="utf-8") as f:
        json.dump(eto_data, f, indent=4, ensure_ascii=False)

    print(f"JSON guardado en: {output}")

if __name__ == "__main__":
    asyncio.run(main())