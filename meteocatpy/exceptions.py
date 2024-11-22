"""METEOCAT API exceptions."""

from __future__ import annotations


class MeteocatError(Exception):
    """Base class for METEOCAT errors."""


class MeteocatTimeout(MeteocatError):
    """Exception raised when API times out."""


class AuthError(MeteocatError):
    """Exception raised when API denies access."""


class ApiError(MeteocatError):
    """Exception raised when data is not provided by API."""


class StationNotFound(MeteocatError):
    """Exception raised when there are no stations close to provided coordinates."""


class TooManyRequests(MeteocatError):
    """Exception raised when max API requests are exceeded."""


class TownNotFound(MeteocatError):
    """Exception raised when there are no towns close to provided coordinates."""