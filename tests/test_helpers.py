"""Tests for Meteocat date helpers."""

from datetime import date, datetime, timedelta, timezone

from meteocatpy.helpers import extract_available_date, parse_api_timestamp


def test_extract_available_date_from_real_message():
    """The documented 400 message lists the available days after 'són:'."""
    message = (
        "La data 07-03-2017 no és vàlida. Els dies disponibles són: "
        "19-04-2017, 20-04-2017 i 21-04-2017"
    )

    assert extract_available_date(message) == date(2017, 4, 21)


def test_extract_available_date_prefers_latest_not_in_the_future():
    """Future dates in the list are ignored in favour of the latest past day."""
    message = "Els dies disponibles són: 26-11-2026, 27-11-2026 i 28-11-2026"

    assert extract_available_date(message, today=date(2026, 11, 27)) == date(
        2026, 11, 27
    )


def test_extract_available_date_without_dates():
    """Messages without dates do not trigger a retry."""
    assert extract_available_date("Bad Request") is None
    assert extract_available_date(None) is None


def test_parse_api_timestamp_preserves_offsets():
    """Existing offsets are preserved and naive values are assumed UTC."""
    parsed = parse_api_timestamp("2026-11-27T12:00:00+02:00")
    assert parsed.utcoffset() == timedelta(hours=2)

    parsed = parse_api_timestamp("2026-11-27T12:00:00Z")
    assert parsed.utcoffset() == timedelta(0)

    parsed = parse_api_timestamp("2026-11-27T12:00:00")
    assert parsed.utcoffset() == timedelta(0)


def test_current_date_is_utc():
    """The day-based API helpers use UTC, matching the API payloads."""
    from meteocatpy.data import MeteocatStationData

    before = datetime.now(timezone.utc).date()
    year, month, day = MeteocatStationData.get_current_date()
    after = datetime.now(timezone.utc).date()

    assert date(year, month, day) in (before, after)
