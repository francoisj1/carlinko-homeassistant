"""
carlinko/decoder.py

Decode CarLinko websocket telemetry.

Based on verified offsets from the working J5 EV dashboard.
"""

from __future__ import annotations

from .telemetry import Telemetry


class CarLinkoDecoder:
    """Decode CarLinko telemetry packets."""

    def decode(self, hex_data: str) -> Telemetry:

        telemetry = Telemetry()

        telemetry.raw_hex = hex_data

        try:
            packet = bytes.fromhex(hex_data)
        except Exception:
            return telemetry

        telemetry.raw_packet = packet

        #
        # Packet too short
        #
        if len(packet) < 52:
            telemetry.update_timestamp()
            return telemetry

        # -------------------------------------------------------
        # VERIFIED OFFSETS
        # (from tools/check_live.py in the dashboard)
        # -------------------------------------------------------

        #
        # HV Battery SOC
        #
        telemetry.battery.soc = packet[28]

        #
        # EV Remaining Range (km)
        #
        telemetry.battery.remaining_range_km = int.from_bytes(
            packet[29:31],
            "big",
        )

        #
        # Auxiliary battery voltage
        #
        telemetry.battery.voltage = (
            int.from_bytes(packet[12:14], "big") / 100.0
        )

        #
        # Odometer
        #
        telemetry.vehicle.odometer_km = int.from_bytes(
            packet[18:21],
            "big",
        )

        #
        # Raw TPMS bytes
        #
        tpms = packet[44:52]

        #
        # Current scaling is still unknown.
        # Store raw values for now.
        #
        telemetry.tyres.fl_pressure = tpms[0]
        telemetry.tyres.fr_pressure = tpms[1]
        telemetry.tyres.rl_pressure = tpms[2]
        telemetry.tyres.rr_pressure = tpms[3]

        telemetry.tyres.fl_temperature = tpms[4]
        telemetry.tyres.fr_temperature = tpms[5]
        telemetry.tyres.rl_temperature = tpms[6]
        telemetry.tyres.rr_temperature = tpms[7]

        #
        # -------------------------------------------------------
        # Fields still to be mapped
        # -------------------------------------------------------
        #
        telemetry.battery.charging = None
        telemetry.battery.charger_connected = None

        telemetry.vehicle.speed_kmh = None

        telemetry.gps.latitude = None
        telemetry.gps.longitude = None

        telemetry.locks.locked = None

        telemetry.update_timestamp()

        return telemetry

    # ---------------------------------------------------------

    @staticmethod
    def dump(packet: bytes):

        print("\nPacket length:", len(packet))
        print("Offset  Hex  Dec")

        for i, value in enumerate(packet):
            print(f"{i:03d}    {value:02X}   {value:3d}")
