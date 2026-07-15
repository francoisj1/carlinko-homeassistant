"""
carlinko-python

Python SDK for the CarLinko connected vehicle platform.

Example
-------
>>> from carlinko import CarLinkoClient
>>>
>>> client = CarLinkoClient(
...     email="user@example.com",
...     password="password",
...     region="sea",
... )
>>>
>>> client.login()
>>> vehicles = client.get_vehicles()
"""

from .client import CarLinkoClient

from .models import (
    User,
    Vehicle,
    VehicleStatus,
    Location,
    WebSocketInfo,
)

from .exceptions import (
    CarLinkoError,
    ApiError,
    AuthenticationError,
    NetworkError,
    VehicleNotFound,
)

__title__ = "carlinko"
__description__ = "Python SDK for the CarLinko connected vehicle platform."
__version__ = "0.1.0"
__author__ = "Francois Janzen van Nieuwenhuizen"
__license__ = "MIT"

__all__ = [
    # Main Client
    "CarLinkoClient",

    # Models
    "User",
    "Vehicle",
    "VehicleStatus",
    "Location",
    "WebSocketInfo",

    # Exceptions
    "CarLinkoError",
    "ApiError",
    "AuthenticationError",
    "NetworkError",
    "VehicleNotFound",
]
