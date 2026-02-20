"""Config flow for Bose SoundTouch Local integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)

class SoundTouchLocalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bose SoundTouch Local."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Check if already configured
            await self.async_set_unique_id(user_input[CONF_HOST])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_NAME): str,
            }),
            errors=errors,
        )

    async def async_step_zeroconf(self, discovery_info):
        """Handle zeroconf discovery."""
        host = discovery_info.host
        name = discovery_info.name.split(".")[0]
        
        await self.async_set_unique_id(host)
        self._abort_if_unique_id_configured()

        self.context.update({
            "title_placeholders": {"name": name},
            "configuration_url": f"http://{host}:{DEFAULT_PORT}",
        })

        return await self.async_step_confirm()

    async def async_step_confirm(self, user_input=None):
        """Handle user-confirmation of discovered device."""
        if user_input is not None:
            return self.async_create_entry(
                title=self.context["title_placeholders"]["name"],
                data={
                    CONF_HOST: self.unique_id,
                    CONF_NAME: self.context["title_placeholders"]["name"],
                }
            )

        return self.async_show_form(
            step_id="confirm",
            description_placeholders={
                "name": self.context["title_placeholders"]["name"]
            }
        )
