"""Basic METEOCAT client example."""

import asyncio
import timeit

from _common import json_dumps
from _secrets import METEOCAT_COORDS, METEOCAT_DATA_DIR, METEOCAT_OPTIONS
import aiohttp

from meteocatpy.exceptions import ApiError, AuthError, TooManyRequests, TownNotFound
from meteocatpy.interface import METEOCAT


async def main():
    """METEOCAT client example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        client = METEOCAT(aiohttp_session, METEOCAT_OPTIONS)

        client.set_api_data_dir(METEOCAT_DATA_DIR)

        try:
            select_start = timeit.default_timer()
            await client.select_coordinates(METEOCAT_COORDS[0], METEOCAT_COORDS[1])
            select_end = timeit.default_timer()
            print(json_dumps(client.data()))
            print(f"Select time: {select_end - select_start}")
            print("***")

            update_start = timeit.default_timer()
            await client.update()
            update_end = timeit.default_timer()
            print(json_dumps(client.data()))
            print(f"Update time: {update_end - update_start}")
        except ApiError:
            print("API data error")
        except AuthError:
            print("API authentication error.")
        except TooManyRequests:
            print("Too many requests.")
        except TownNotFound:
            print("Town not found.")


if __name__ == "__main__":
    asyncio.run(main())