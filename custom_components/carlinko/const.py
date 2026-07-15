"""
Constants for the CarLinko Home Assistant integration.
"""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "carlinko"

NAME = "CarLinko"

VERSION = "0.1.0"

MANUFACTURER = "CarLinko"

#
# Configuration
#

CONF_EMAIL = "email"
CONF_PASSWORD = "password"
CONF_REGION = "region"

DEFAULT_REGION = "saf"

#
# Coordinator
#
# Although telemetry is pushed via WebSocket, Home Assistant
# still expects a coordinator. This interval acts as a fallback.
#

UPDATE_INTERVAL = timedelta(minutes=5)

#
# Platforms
#

PLATFORMS: list[str] = [
    "sensor",
    "binary_sensor",
]

#
# Entity names
#

ATTR_BATTERY = "Battery"
ATTR_EV_RANGE = "EV Range"
ATTR_MODEL = "Model"
ATTR_VIN = "VIN"
ATTR_LAST_UPDATE = "Last Update"
ATTR_CONNECTED = "Connected"

#
# Sensor keys
#

SENSOR_BATTERY = "battery_soc"
SENSOR_EV_RANGE = "ev_range"
SENSOR_MODEL = "vehicle_model"
SENSOR_VIN = "vin"
SENSOR_LAST_UPDATE = "last_update"

#
# Binary sensor keys
#

BINARY_CONNECTED = "connected"

#
# Services
#

SERVICE_REFRESH = "refresh"

#
# Logging
#

LOGGER_NAME = "custom_components.carlinko"

#
# Regions
#
# More can easily be added as additional CarLinko
# deployments are confirmed.
#

REGIONS = {
    "saf": "South Africa",
    "sea": "South East Asia",
    "eu": "Europe",
}

#
# Vehicle defaults
#

UNKNOWN = "Unknown"

#
# Device identifiers
#

DEVICE_IDENTIFIER = DOMAIN

#
# Coordinator data keys
#

DATA_CLIENT = "client"
DATA_TELEMETRY = "telemetry"
DATA_VEHICLE = "vehicle"

#
# Configuration entry version
#

CONFIG_VERSION = 1
