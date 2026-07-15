"""
Sensor platform for the CarLinko integration.
"""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfLength,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN
from .coordinator import CarLinkoCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up CarLinko sensors."""

    coordinator: CarLinkoCoordinator = hass.data[
        DOMAIN
    ][entry.entry_id]["coordinator"]

    vehicle = hass.data[
        DOMAIN
    ][entry.entry_id]["vehicle"]

    async_add_entities(
        [
            BatterySensor(coordinator, vehicle),
            RangeSensor(coordinator, vehicle),
            ModelSensor(coordinator, vehicle),
            VinSensor(coordinator, vehicle),
            LastUpdateSensor(coordinator, vehicle),
        ]
    )


class CarLinkoSensor(CoordinatorEntity, SensorEntity):
    """Base class for all CarLinko sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CarLinkoCoordinator,
        vehicle,
    ):

        super().__init__(coordinator)

        self.vehicle = vehicle

        self._attr_device_info = DeviceInfo(
            identifiers={
                (DOMAIN, vehicle.id),
            },
            manufacturer=vehicle.brand,
            model=vehicle.model,
            name=f"{vehicle.brand} {vehicle.model}",
            sw_version="SDK",
        )


class BatterySensor(CarLinkoSensor):
    """Battery SOC."""

    _attr_name = "Battery"

    _attr_unique_id = "carlinko_battery"

    _attr_native_unit_of_measurement = PERCENTAGE

    _attr_device_class = SensorDeviceClass.BATTERY

    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):

        return self.coordinator.battery_soc


class RangeSensor(CarLinkoSensor):
    """Remaining EV range."""

    _attr_name = "EV Range"

    _attr_unique_id = "carlinko_ev_range"

    _attr_native_unit_of_measurement = UnitOfLength.KILOMETERS

    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):

        return self.coordinator.ev_range


class ModelSensor(CarLinkoSensor):
    """Vehicle model."""

    _attr_name = "Model"

    _attr_unique_id = "carlinko_model"

    @property
    def native_value(self):

        return self.vehicle.model


class VinSensor(CarLinkoSensor):
    """VIN."""

    _attr_name = "VIN"

    _attr_unique_id = "carlinko_vin"

    @property
    def native_value(self):

        return self.vehicle.vin


class LastUpdateSensor(CarLinkoSensor):
    """Timestamp of latest telemetry."""

    _attr_name = "Last Update"

    _attr_unique_id = "carlinko_last_update"

    @property
    def native_value(self):

        return self.coordinator.last_update

