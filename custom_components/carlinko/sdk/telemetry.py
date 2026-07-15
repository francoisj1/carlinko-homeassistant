"""
carlinko/telemetry.py

Telemetry models for CarLinko vehicles.

These classes represent the current state of a vehicle and are populated
by decoder.py from the websocket telemetry stream.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# ------------------------------------------------------------------
# Battery
# ------------------------------------------------------------------

@dataclass
class BatteryStatus:

    soc: Optional[int] = None

    remaining_range_km: Optional[int] = None

    voltage: Optional[float] = None

    current: Optional[float] = None

    power_kw: Optional[float] = None

    temperature_c: Optional[float] = None

    health_percent: Optional[int] = None

    charging: bool = False

    charger_connected: bool = False

    charge_voltage: Optional[float] = None

    charge_current: Optional[float] = None

    charge_power_kw: Optional[float] = None

    charge_target_percent: Optional[int] = None

    minutes_remaining: Optional[int] = None


# ------------------------------------------------------------------
# Vehicle
# ------------------------------------------------------------------

@dataclass
class VehicleStatus:

    ignition: bool = False

    ready: bool = False

    parked: bool = True

    speed_kmh: Optional[int] = None

    odometer_km: Optional[int] = None

    gear: Optional[str] = None

    drive_mode: Optional[str] = None


# ------------------------------------------------------------------
# GPS
# ------------------------------------------------------------------

@dataclass
class GPSStatus:

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    altitude: Optional[int] = None

    heading: Optional[int] = None

    speed_kmh: Optional[int] = None

    accuracy: Optional[float] = None

    timestamp: Optional[datetime] = None


# ------------------------------------------------------------------
# Climate
# ------------------------------------------------------------------

@dataclass
class ClimateStatus:

    hvac_on: bool = False

    ac_on: bool = False

    fan_speed: Optional[int] = None

    inside_temperature: Optional[float] = None

    outside_temperature: Optional[float] = None


# ------------------------------------------------------------------
# Doors
# ------------------------------------------------------------------

@dataclass
class DoorStatus:

    driver: bool = False

    passenger: bool = False

    rear_left: bool = False

    rear_right: bool = False

    bonnet: bool = False

    boot: bool = False


# ------------------------------------------------------------------
# Windows
# ------------------------------------------------------------------

@dataclass
class WindowStatus:

    driver: bool = False

    passenger: bool = False

    rear_left: bool = False

    rear_right: bool = False

    sunroof: bool = False


# ------------------------------------------------------------------
# Locks
# ------------------------------------------------------------------

@dataclass
class LockStatus:

    locked: bool = False

    auto_locked: bool = False

    key_detected: bool = False


# ------------------------------------------------------------------
# Lights
# ------------------------------------------------------------------

@dataclass
class LightStatus:

    headlights: bool = False

    parking: bool = False

    high_beam: bool = False

    fog_front: bool = False

    fog_rear: bool = False

    hazard: bool = False


# ------------------------------------------------------------------
# Tyres
# ------------------------------------------------------------------

@dataclass
class TyreStatus:

    fl_pressure: Optional[float] = None

    fr_pressure: Optional[float] = None

    rl_pressure: Optional[float] = None

    rr_pressure: Optional[float] = None

    fl_temperature: Optional[int] = None

    fr_temperature: Optional[int] = None

    rl_temperature: Optional[int] = None

    rr_temperature: Optional[int] = None


# ------------------------------------------------------------------
# Vehicle Health
# ------------------------------------------------------------------

@dataclass
class VehicleHealth:

    low_battery: bool = False

    service_due: bool = False

    tpms_warning: bool = False

    battery_fault: bool = False

    motor_fault: bool = False

    brake_fault: bool = False

    airbag_fault: bool = False

    abs_fault: bool = False


# ------------------------------------------------------------------
# Main Telemetry Object
# ------------------------------------------------------------------

@dataclass
class Telemetry:

    battery: BatteryStatus = field(default_factory=BatteryStatus)

    vehicle: VehicleStatus = field(default_factory=VehicleStatus)

    gps: GPSStatus = field(default_factory=GPSStatus)

    climate: ClimateStatus = field(default_factory=ClimateStatus)

    doors: DoorStatus = field(default_factory=DoorStatus)

    windows: WindowStatus = field(default_factory=WindowStatus)

    locks: LockStatus = field(default_factory=LockStatus)

    lights: LightStatus = field(default_factory=LightStatus)

    tyres: TyreStatus = field(default_factory=TyreStatus)

    health: VehicleHealth = field(default_factory=VehicleHealth)

    last_update: Optional[datetime] = None

    raw_packet: bytes = b""

    raw_hex: str = ""

    # ----------------------------------------------------------

    @property
    def connected(self) -> bool:

        return self.last_update is not None

    # ----------------------------------------------------------

    def update_timestamp(self):

        self.last_update = datetime.utcnow()

    # ----------------------------------------------------------

    def to_dict(self):

        return {
            "battery_soc": self.battery.soc,
            "range_km": self.battery.remaining_range_km,
            "charging": self.battery.charging,
            "charger_connected": self.battery.charger_connected,
            "speed": self.vehicle.speed_kmh,
            "odometer": self.vehicle.odometer_km,
            "latitude": self.gps.latitude,
            "longitude": self.gps.longitude,
            "locked": self.locks.locked,
            "last_update": self.last_update,
        }
