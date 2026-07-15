"""
carlinko/models.py

Data models for the CarLinko API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ------------------------------------------------------------------
# Base Model
# ------------------------------------------------------------------


@dataclass(slots=True)
class BaseModel:
    """
    Base model that preserves the original API response.
    """

    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    def as_dict(self) -> dict[str, Any]:
        """Return the original API response."""
        return dict(self.raw)


# ------------------------------------------------------------------
# User
# ------------------------------------------------------------------


@dataclass(slots=True)
class User(BaseModel):

    id: str | None = None
    nickname: str | None = None
    email: str | None = None
    phone: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "User":

        return cls(
            id=data.get("id") or data.get("userId"),
            nickname=data.get("nickname"),
            email=data.get("email"),
            phone=data.get("phone"),
            raw=data,
        )


# ------------------------------------------------------------------
# Vehicle
# ------------------------------------------------------------------


@dataclass(slots=True)
class Vehicle(BaseModel):

    #
    # Vehicle identifiers
    #

    id: str | None = None
    vin: str | None = None

    #
    # CarLinko identifiers
    #

    device_sn: str | None = None
    device_id: str | None = None
    device_name: str | None = None

    #
    # Vehicle information
    #

    nickname: str | None = None

    brand: str | None = None
    model: str | None = None
    model_code: str |None = None

    color: str | None = None
    year: int | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Vehicle":

        device_id = data.get("deviceId")
        device_name = data.get("deviceName")

        #
        # Different CarLinko deployments use different
        # field names for the websocket identifier.
        #

        device_sn = (
            data.get("deviceSn")
            or data.get("terminalSn")
            or device_id
            or device_name
        )

        return cls(
            id=(
                data.get("vehicleId")
                or data.get("id")
            ),

            vin=data.get("vin"),

            device_sn=device_sn,
            device_id=device_id,
            device_name=device_name,

            nickname=data.get("nickname"),

            brand=data.get("brand"),

            model=(
                data.get("model")
                or data.get("vehicleModel")
            ),

            model_code=data.get("modelCode"),

            color=data.get("color"),

            year=data.get("year"),

            raw=data,
        )


# ------------------------------------------------------------------
# Vehicle Status
# ------------------------------------------------------------------


@dataclass(slots=True)
class VehicleStatus(BaseModel):

    battery_soc: float | None = None

    fuel_level: float | None = None

    charging: bool | None = None

    plugged_in: bool | None = None

    ev_range_km: float | None = None

    total_range_km: float | None = None

    odometer_km: float | None = None

    speed_kmh: float | None = None

    latitude: float | None = None

    longitude: float | None = None

    last_update: datetime | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "VehicleStatus":

        return cls(
            battery_soc=data.get("soc"),

            fuel_level=data.get("fuelLevel"),

            charging=data.get("charging"),

            plugged_in=data.get("plugged"),

            ev_range_km=(
                data.get("evRange")
                or data.get("range")
            ),

            total_range_km=data.get("totalRange"),

            odometer_km=data.get("odometer"),

            speed_kmh=data.get("speed"),

            latitude=data.get("latitude"),

            longitude=data.get("longitude"),

            last_update=None,

            raw=data,
        )


# ------------------------------------------------------------------
# Location
# ------------------------------------------------------------------


@dataclass(slots=True)
class Location(BaseModel):

    latitude: float | None = None

    longitude: float | None = None

    speed: float | None = None

    heading: float | None = None

    timestamp: datetime | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Location":

        return cls(
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            speed=data.get("speed"),
            heading=data.get("heading"),
            timestamp=None,
            raw=data,
        )


# ------------------------------------------------------------------
# WebSocket Connection
# ------------------------------------------------------------------


@dataclass(slots=True)
class WebSocketInfo(BaseModel):

    host: str | None = None

    port: int | None = None

    path: str | None = None

    token: str | None = None

    ssl: bool = True

    url: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "WebSocketInfo":

        url = (
            data.get("url")
            or data.get("data")
            or data.get("host")
        )

        return cls(
            host=data.get("host"),
            port=data.get("port"),
            path=data.get("path"),
            token=data.get("token"),
            ssl=data.get("ssl", True),
            url=url,
            raw=data,
        )
