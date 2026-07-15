"""
CarLinko Home Assistant Integration.

Initialises the CarLinko SDK and DataUpdateCoordinator.
"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    DATA_CLIENT,
    DOMAIN,
)

from .coordinator import CarLinkoCoordinator
from .sdk.client import CarLinkoClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """
    Set up the integration from configuration.yaml.

    (Not used - configuration is handled via Config Flow.)
    """
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """
    Set up CarLinko from a Config Entry.
    """

    hass.data.setdefault(DOMAIN, {})

    email = entry.data["email"]
    password = entry.data["password"]
    region = entry.data["region"]

    _LOGGER.info("Connecting to CarLinko cloud...")

    #
    # Create SDK client
    #

    client = CarLinkoClient(
        email=email,
        password=password,
        region=region,
        debug=False,
    )

    #
    # Login
    #

    await hass.async_add_executor_job(client.login)

    #
    # Read vehicles
    #

    vehicles = await hass.async_add_executor_job(
        client.get_vehicles
    )

    if not vehicles:
        raise RuntimeError("No vehicles found.")

    vehicle = vehicles[0]

    #
    # Start websocket
    #

    await hass.async_add_executor_job(
        client.start_live_updates,
        vehicle,
    )

    #
    # Coordinator
    #

    coordinator = CarLinkoCoordinator(
        hass=hass,
        client=client,
        vehicle=vehicle,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: client,
        "vehicle": vehicle,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    _LOGGER.info("CarLinko integration loaded successfully.")

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """
    Unload a config entry.
    """

    data = hass.data[DOMAIN].pop(entry.entry_id)

    client: CarLinkoClient = data[DATA_CLIENT]

    try:
        await hass.async_add_executor_job(
            client.stop_live_updates
        )
    except Exception:
        pass

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        _LOGGER.info("CarLinko unloaded.")

    return unload_ok

