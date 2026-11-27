"""Meteocat Helpers."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import date, datetime, timezone
from typing import Any
import re
import unicodedata
from zoneinfo import ZoneInfo

import aiohttp

TZ_UTC = ZoneInfo("UTC")


def dict_nested_value(data: dict[str, Any] | None, keys: list[str] | None) -> Any:
    """Get value from dict with nested keys."""
    if keys is None or len(keys) == 0:
        return None
    for key in keys or {}:
        if data is not None:
            data = data.get(key)
    return data


def get_current_datetime(tz: ZoneInfo = TZ_UTC, replace: bool = True) -> datetime:
    """Return current datetime in UTC."""
    cur_dt = datetime.now(tz=tz)
    if replace:
        cur_dt = cur_dt.replace(minute=0, second=0, microsecond=0)
    return cur_dt


def parse_api_timestamp(timestamp: str, tz: ZoneInfo = TZ_UTC) -> datetime:
    """Parse an API timestamp, assuming a timezone only when it is naive."""
    normalized = f"{timestamp[:-1]}+00:00" if timestamp.endswith("Z") else timestamp
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=tz)
    return parsed


_DATE_PATTERN = re.compile(r"\b(\d{2})-(\d{2})-(\d{4})\b")


def extract_available_date(
    message: str | None, today: date | None = None
) -> date | None:
    """Extract the most recent valid date from a Meteocat 400 message.

    The API returns messages such as:
    "La data 07-03-2017 no és vàlida. Els dies disponibles són:
    19-04-2017, 20-04-2017 i 21-04-2017".
    """
    if not message:
        return None

    dates: list[date] = []
    for day, month, year in _DATE_PATTERN.findall(message):
        try:
            dates.append(date(int(year), int(month), int(day)))
        except ValueError:
            continue
    if not dates:
        return None

    reference = today or datetime.now(timezone.utc).date()
    past_dates = [value for value in dates if value <= reference]
    return max(past_dates or dates)


def slugify(value: str, allow_unicode: bool = False) -> str:
    """Convert string to a valid file name."""
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s]", "-", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


@asynccontextmanager
async def session_context(
    session: aiohttp.ClientSession | None,
) -> AsyncIterator[aiohttp.ClientSession]:
    """Yield the provided session or a temporary one."""
    if session is not None:
        yield session
        return
    async with aiohttp.ClientSession() as own_session:
        yield own_session
