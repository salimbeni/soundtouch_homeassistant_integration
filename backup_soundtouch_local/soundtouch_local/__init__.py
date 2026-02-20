"""The Bose SoundTouch Local integration."""
import logging
from bosesoundtouchapi import SoundTouchDevice

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, DATA_SOUNDTOUCH

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.MEDIA_PLAYER]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bose SoundTouch Local from a config entry."""
    host = entry.data[CONF_HOST]

    try:
        # Initialize the device
        device = await hass.async_add_executor_job(SoundTouchDevice, host)
        
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = device

        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        return True
    except Exception as ex:
        _LOGGER.error("Could not connect to Bose SoundTouch at %s: %s", host, ex)
        return False

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
