"""
carlinko/client.py

Main CarLinko SDK client.
"""

from __future__ import annotations

from pprint import pprint

from .auth import Authentication
from .decoder import CarLinkoDecoder
from .exceptions import (
    ApiError,
    VehicleNotFound,
)
from .models import (
    User,
    Vehicle,
)
from .telemetry import Telemetry
from .websocket import CarLinkoWebSocket


class CarLinkoClient:

    def __init__(
        self,
        email: str,
        password: str,
        region: str = "saf",
        *,
        timeout: int = 20,
        debug: bool = False,
    ):

        self.auth = Authentication(
            account=email,
            password=password,
            region=region,
            timeout=timeout,
        )

        self.http = self.auth.client

        self.debug = debug

        self.decoder = CarLinkoDecoder()

        self.telemetry = Telemetry()

        self.websocket = None

    # ----------------------------------------------------------
    # Authentication
    # ----------------------------------------------------------

    def login(self):

        return self.auth.login()

    @property
    def token(self):

        return self.auth.token

    @property
    def authenticated(self):

        return self.auth.token is not None

    # ----------------------------------------------------------
    # REST Request
    # ----------------------------------------------------------

    def request(
        self,
        method,
        endpoint,
        *,
        params=None,
        json=None,
    ):

        body = json or {}

        response = self.http.request(
            method=method,
            url=self.auth.api_base + endpoint,
            params=params,
            json=json,
            headers=self.auth.headers(body),
        )

        response.raise_for_status()

        payload = response.json()

        if self.debug:

            print("\nREST RESPONSE")
            pprint(payload)

        if str(payload.get("code")) != "0000":
            raise ApiError(payload.get("msg"))

        return payload.get("data")

    # ----------------------------------------------------------
    # User
    # ----------------------------------------------------------

    def get_profile(self):

        return User.from_api(
            self.request(
                "GET",
                "/user/info",
            )
        )

    # ----------------------------------------------------------
    # Vehicles
    # ----------------------------------------------------------

    def get_vehicles(self):

        data = self.request(
            "GET",
            "/user/vehicle",
        )

        if not data:
            return []

        vehicles = []

        for item in data:

            if self.debug:

                print("\nVehicle JSON")
                pprint(item)

            vehicles.append(
                Vehicle.from_api(item)
            )

        return vehicles

    def get_vehicle(self, vehicle_id):

        for vehicle in self.get_vehicles():

            if str(vehicle.id) == str(vehicle_id):
                return vehicle

        raise VehicleNotFound(vehicle_id)

    # ----------------------------------------------------------
    # Terminal
    # ----------------------------------------------------------

    def get_terminal(self, vehicle_id):

        return self.request(
            "GET",
            f"/user/vehicle/terminal/{vehicle_id}",
        )

    # ----------------------------------------------------------
    # Websocket Discovery
    # ----------------------------------------------------------

    def get_websocket(self, device_sn):

        return self.request(
            "GET",
            f"/netty/getConnect/2/{device_sn}",
        )

    # ----------------------------------------------------------
    # Raw REST
    # ----------------------------------------------------------

    def raw(
        self,
        endpoint,
        *,
        method="GET",
        params=None,
        json=None,
    ):

        return self.request(
            method,
            endpoint,
            params=params,
            json=json,
        )

    # ----------------------------------------------------------
    # Live Telemetry
    # ----------------------------------------------------------

    def start_live_updates(
        self,
        vehicle: Vehicle,
    ):

        #
        # Try every known identifier.
        #

        device = (
            getattr(vehicle, "device_sn", None)
            or getattr(vehicle, "device_id", None)
            or getattr(vehicle, "device_name", None)
        )

        if device is None:
            raise RuntimeError(
                "Vehicle does not contain a device identifier."
            )

        #
        # Discover websocket.
        #

        ws = self.get_websocket(device)

        if isinstance(ws, dict):
            ws_url = (
                ws.get("url")
                or ws.get("data")
                or next(iter(ws.values()))
            )
        else:
            ws_url = ws

        self.websocket = CarLinkoWebSocket(
            url=ws_url,
            token=self.token,
            vehicle_id=vehicle.id,
            device_sn=device,
            debug=self.debug,
        )

        self.websocket.add_callback(
            self._telemetry_callback
        )

        self.websocket.connect()

    # ----------------------------------------------------------

    def stop_live_updates(self):

        if self.websocket:

            self.websocket.close()

            self.websocket = None

    # ----------------------------------------------------------

    def get_live_telemetry(self):

        return self.telemetry

    # ----------------------------------------------------------
    # Internal callback
    # ----------------------------------------------------------

    def _telemetry_callback(self, packet):

        if self.debug:

            print("\nWS PACKET")
            pprint(packet)

        if not isinstance(packet, dict):
            return

        if packet.get("action") != 6:
            return

        data = packet.get("data")

        if not isinstance(data, str):
            return

        telemetry = self.decoder.decode(data)

        telemetry.raw_hex = data

        telemetry.update_timestamp()

        self.telemetry = telemetry

    # ----------------------------------------------------------
    # Async wrappers for Home Assistant
    # ----------------------------------------------------------

    async def login_async(self):
        """Async wrapper around login()."""
        import asyncio
        return await asyncio.to_thread(self.login)

    async def get_profile_async(self):
        """Async wrapper around get_profile()."""
        import asyncio
        return await asyncio.to_thread(self.get_profile)

    async def get_vehicles_async(self):
        """Async wrapper around get_vehicles()."""
        import asyncio
        return await asyncio.to_thread(self.get_vehicles)

    async def get_vehicle_async(self, vehicle_id):
        """Async wrapper around get_vehicle()."""
        import asyncio
        return await asyncio.to_thread(
            self.get_vehicle,
            vehicle_id,
        )

    async def get_terminal_async(self, vehicle_id):
        """Async wrapper around get_terminal()."""
        import asyncio
        return await asyncio.to_thread(
            self.get_terminal,
            vehicle_id,
        )

    async def get_websocket_async(self, device_sn):
        """Async wrapper around get_websocket()."""
        import asyncio
        return await asyncio.to_thread(
            self.get_websocket,
            device_sn,
        )

    async def start_live_updates_async(self, vehicle):
        """Async wrapper around start_live_updates()."""
        import asyncio
        return await asyncio.to_thread(
            self.start_live_updates,
            vehicle,
        )

    async def stop_live_updates_async(self):
        """Async wrapper around stop_live_updates()."""
        import asyncio
        return await asyncio.to_thread(
            self.stop_live_updates,
        )

    async def get_live_telemetry_async(self):
        """Async wrapper around get_live_telemetry()."""
        import asyncio
        return await asyncio.to_thread(
            self.get_live_telemetry,
        )

    async def raw_async(
        self,
        endpoint,
        *,
        method="GET",
        params=None,
        json=None,
    ):
        """Async wrapper around raw()."""
        import asyncio
        return await asyncio.to_thread(
            self.raw,
            endpoint,
            method=method,
            params=params,
            json=json,
        )
