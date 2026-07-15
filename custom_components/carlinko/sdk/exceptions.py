"""
carlinko/exceptions.py

Custom exceptions for the CarLinko SDK.
"""


class CarLinkoError(Exception):
    """Base exception for all CarLinko errors."""


class ApiError(CarLinkoError):
    """Raised when the CarLinko API returns an error."""


class AuthenticationError(CarLinkoError):
    """Raised when authentication fails."""


class NetworkError(CarLinkoError):
    """Raised when a network request fails."""


class VehicleNotFound(CarLinkoError):
    """Raised when a requested vehicle cannot be found."""


class SignatureError(CarLinkoError):
    """Raised when request signing fails."""