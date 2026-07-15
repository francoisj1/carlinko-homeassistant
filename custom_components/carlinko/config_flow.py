"""
Config Flow for the CarLinko integration.
"""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_REGION,
    DEFAULT_REGION,
    DOMAIN,
    REGIONS,
)

from .sdk.client import CarLinkoClient

_LOGGER = logging.getLogger(__name__)


class CannotConnect(Exception):
    """Unable to connect."""


class InvalidAuth(Exception):
    """Invalid authentication."""


async def validate_input(data: dict) -> dict:
    """
    Validate the user's credentials by logging into CarLinko.
    """

    client = CarLinkoClient(
        email=data[CONF_EMAIL],
        password=data[CONF_PASSWORD],
        region=data[CONF_REGION],
        debug=False,
    )

    try:
        await client.login_async()

        vehicles = await client.get_vehicles_async()

        if not vehicles:
            raise CannotConnect("No vehicles found.")

        vehicle = vehicles[0]

        return {
            "title": f"{vehicle.brand} {vehicle.model}",
            "vehicle": vehicle,
        }

    except Exception as err:

        message = str(err).lower()

        if (
            "password" in message
            or "login" in message
            or "authentication" in message
            or "401" in message
        ):
            raise InvalidAuth from err

        raise CannotConnect from err


class CarLinkoConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """
    CarLinko Config Flow.
    """

    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ):

        errors = {}

        if user_input is not None:

            #
            # Prevent duplicate entries.
            #

            await self.async_set_unique_id(
                user_input[CONF_EMAIL].lower()
            )

            self._abort_if_unique_id_configured()

            try:

                info = await validate_input(
                    user_input
                )

                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )

            except InvalidAuth:

                errors["base"] = "invalid_auth"

            except CannotConnect:

                errors["base"] = "cannot_connect"

            except Exception:

                _LOGGER.exception(
                    "Unexpected exception"
                )

                errors["base"] = "unknown"

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_EMAIL,
                ): str,

                vol.Required(
                    CONF_PASSWORD,
                ): str,

                vol.Required(
                    CONF_REGION,
                    default=DEFAULT_REGION,
                ): vol.In(REGIONS),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):

        return CarLinkoOptionsFlow(config_entry)


class CarLinkoOptionsFlow(
    config_entries.OptionsFlow,
):
    """
    Options Flow.
    """

    def __init__(self, config_entry):

        self.config_entry = config_entry

    async def async_step_init(
        self,
        user_input=None,
    ):

        if user_input is not None:

            return self.async_create_entry(
                title="",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_REGION,
                    default=self.config_entry.options.get(
                        CONF_REGION,
                        self.config_entry.data.get(
                            CONF_REGION,
                            DEFAULT_REGION,
                        ),
                    ),
                ): vol.In(REGIONS),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )

