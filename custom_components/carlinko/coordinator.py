"""
DataUpdateCoordinator for the CarLinko integration.
"""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .sdk.client import CarLinkoClient
from .sdk.models import Vehicle

_LOGGER = logging.getLogger(__name__)


class CarLinkoCoordinator(DataUpdateCoordinator):
    """Coordinates data between the SDK and Home Assistant."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: CarLinkoClient,
        vehicle: Vehicle,
    ) -> None:

        self.client = client
        self.vehicle = vehicle

        super().__init__(
            hass,
            _LOGGER,
            name="CarLinko",
            update_interval=timedelta(seconds=5),
        )

    async def _async_update_data(self):
        """
        Return the latest telemetry already stored by the SDK.

        This does NOT contact the cloud.
        The SDK's WebSocket continuously updates the telemetry object.
        """

        try:
            telemetry = await self.client.get_live_telemetry_async()

            if telemetry is None:
                raise UpdateFailed(
                    "No telemetry has been received yet."
                )

            return telemetry

        except Exception as err:
            raise UpdateFailed(str(err)) from err

    @property
    def connected(self) -> bool:
        """Return websocket connection state."""

        try:
            return self.client.websocket is not None
        except Exception:
            return False

    @property
    def battery_soc(self):

        if self.data is None:
            return None

        return self.data.battery.soc

    @property
    def ev_range(self):

        if self.data is None:
            return None

        return self.data.battery.remaining_range_km

    @property
    def last_update(self):

        if self.data is None:
            return None

        return self.data.last_update

    @property
    def vehicle_name(self):

        return f"{self.vehicle.brand} {self.vehicle.model}"

    @property
    def vin(self):

        return self.vehicle.vin

