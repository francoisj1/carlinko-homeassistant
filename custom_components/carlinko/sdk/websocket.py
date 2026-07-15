"""
carlinko/websocket.py

CarLinko realtime websocket client.
"""

from __future__ import annotations

import json
import threading
import time

import websocket


class CarLinkoWebSocket:
    """
    CarLinko realtime websocket client.
    """

    RECONNECT_DELAY = 5

    def __init__(
        self,
        url: str,
        token: str,
        vehicle_id: str,
        device_sn: str,
        *,
        debug: bool = False,
    ):

        self.url = (
            url.replace("http://", "ws://")
               .replace("https://", "wss://")
        )

        self.token = token
        self.vehicle_id = str(vehicle_id)
        self.device_sn = str(device_sn)

        self.debug = debug

        self.ws = None
        self.connected = False
        self.running = False

        self.callbacks = []

    # ---------------------------------------------------------

    def add_callback(self, callback):

        if callback not in self.callbacks:
            self.callbacks.append(callback)

    # ---------------------------------------------------------

    def remove_callback(self, callback):

        if callback in self.callbacks:
            self.callbacks.remove(callback)

    # ---------------------------------------------------------

    def connect(self):

        self.running = True

        thread = threading.Thread(
            target=self._run,
            daemon=True,
        )

        thread.start()

    # ---------------------------------------------------------

    def _run(self):

        while self.running:

            if self.debug:
                print(f"\nConnecting to {self.url}")

            self.ws = websocket.WebSocketApp(
                self.url,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
            )

            self.ws.run_forever()

            if self.running:

                if self.debug:
                    print(
                        f"Disconnected - reconnecting in "
                        f"{self.RECONNECT_DELAY} seconds..."
                    )

                time.sleep(self.RECONNECT_DELAY)

    # ---------------------------------------------------------

    def close(self):

        self.running = False
        self.connected = False

        if self.ws:
            self.ws.close()

    # ---------------------------------------------------------

    def send(self, payload):

        if not self.connected:
            return

        if isinstance(payload, dict):
            payload = json.dumps(payload)

        if self.debug:

            print("\nSEND")
            print(payload)

        self.ws.send(payload)

    # ---------------------------------------------------------

    def authenticate(self):

        self.send(
            {
                "action": 1,
                "data": {
                    "token": self.token,
                    "vehicleId": self.vehicle_id,
                },
            }
        )

    # ---------------------------------------------------------

    def subscribe(self):

        self.send(
            {
                "action": 0,
                "data": {
                    "sn": self.device_sn,
                },
            }
        )

    # ---------------------------------------------------------

    def request_telemetry(self):

        self.send(
            {
                "action": 6
            }
        )

    # ---------------------------------------------------------

    def _on_open(self, ws):

        self.connected = True

        if self.debug:
            print("✓ WebSocket connected")

        #
        # Authenticate
        #

        self.authenticate()

        time.sleep(0.5)

        #
        # Subscribe
        #

        self.subscribe()

        time.sleep(0.5)

        #
        # Request first telemetry packet
        #

        self.request_telemetry()

    # ---------------------------------------------------------

    def _on_message(self, ws, message):

        if self.debug:

            print("\nRECEIVED")
            print(message)

        try:

            packet = json.loads(message)

        except Exception:

            packet = message

        #
        # Forward the packet to registered callbacks.
        # The client is responsible for decoding.
        #

        for callback in list(self.callbacks):

            try:
                callback(packet)

            except Exception as exc:

                print(f"Callback error: {exc}")

    # ---------------------------------------------------------

    def _on_error(self, ws, error):

        if self.debug:

            print("\nWebSocket error")

        print(error)

    # ---------------------------------------------------------

    def _on_close(
        self,
        ws,
        status_code,
        message,
    ):

        self.connected = False

        if self.debug:

            print(
                f"\nWebSocket closed "
                f"({status_code}) {message}"
            )

    # ---------------------------------------------------------

    @property
    def is_connected(self):

        return self.connected
