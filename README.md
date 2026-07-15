ARCHITECTURE

CarLinko Cloud
        │
        │ HTTPS / REST
        ▼
 ┌───────────────────────────┐
 │ Authentication            │
 │ Vehicle Discovery         │
 │ Vehicle Information       │
 └─────────────┬─────────────┘
               │
               │ WebSocket URL
               ▼
 ┌───────────────────────────┐
 │ Live WebSocket Connection │
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │ Packet Decoder            │
 │ Telemetry Model           │
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │ CarLinko SDK              │
 │ (Python Library)          │
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │ Home Assistant            │
 │ DataUpdateCoordinator     │
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │ Sensors                   │
 │ Binary Sensors            │
 │ Diagnostics               │
 └───────────────────────────┘



 Repository Structure


custom_components/
└── carlinko/
    ├── __init__.py
    ├── manifest.json
    ├── const.py
    ├── config_flow.py
    ├── coordinator.py
    ├── sensor.py
    ├── binary_sensor.py
    ├── diagnostics.py
    ├── strings.json
    ├── translations/
    │   └── en.json
    │
    └── sdk/
        ├── auth.py
        ├── client.py
        ├── websocket.py
        ├── decoder.py
        ├── telemetry.py
        ├── models.py
        ├── session.py
        ├── exceptions.py
        └── __init__.py

The SDK is completely independent of Home Assistant.

Responsibilities include:

Authentication
REST API communication
Vehicle discovery
WebSocket connection
Packet decoding
Telemetry model
Live telemetry updates

The SDK can be reused in:

Python scripts
Command line tools
Flask/FastAPI applications
Other home automation platforms
Home Assistant Integration

The Home Assistant layer contains no API logic.

Its responsibilities are:

Configuration Flow
Device Registry
Entity creation
Coordinator
Diagnostics
Services
Home Assistant specific functionality



DATA FLOW
----------

Login

↓

Authentication Token

↓

Retrieve Vehicle List

↓

Retrieve Device Serial Number

↓

Retrieve WebSocket URL

↓

Open WebSocket

↓

Receive Binary Packets

↓

Decode Telemetry

↓

Update Telemetry Object

↓

Coordinator

↓

Home Assistant Entities

↓

Dashboard


----------------------
Current Telemetry


The current prototype exposes:

Battery State of Charge (SOC)
Remaining EV Range
Vehicle Model
VIN
Last Telemetry Update

Additional telemetry fields such as charging state, fuel level, GPS location, odometer, tyre pressures, climate status, and door/lock state will be added as they are decoded.


