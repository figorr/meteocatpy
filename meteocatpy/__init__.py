"""METEOCAT API.

Python Package to collect data from Meteocat API and interact with Meteocat Home Assistant Integration
SPDX-License-Identifier: Apache-2.0

For more details about this api, please refer to the documentation at
https://gitlab.com/figorr/meteocatpy
"""

# meteocatpy/__init__.py
from .client import MeteocatClient

__all__ = ["MeteocatClient"]
