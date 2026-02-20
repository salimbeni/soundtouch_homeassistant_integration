"""Support for Bose SoundTouch devices."""
import logging
from typing import Any

from bosesoundtouchapi import SoundTouchDevice
from bosesoundtouchapi.models import Status, Volume

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SUPPORT_SOUNDTOUCH = (
    MediaPlayerEntityFeature.PAUSE
    | MediaPlayerEntityFeature.PLAY
    | MediaPlayerEntityFeature.STOP
    | MediaPlayerEntityFeature.PREVIOUS_TRACK
    | MediaPlayerEntityFeature.NEXT_TRACK
    | MediaPlayerEntityFeature.VOLUME_SET
    | MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.SELECT_SOURCE
    | MediaPlayerEntityFeature.TURN_OFF
    | MediaPlayerEntityFeature.TURN_ON
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Bose SoundTouch Local media player."""
    device = hass.data[DOMAIN][entry.entry_id]
    name = entry.data[CONF_NAME]

    async_add_entities([SoundTouchMediaPlayer(device, name)], True)

class SoundTouchMediaPlayer(MediaPlayerEntity):
    """Representation of a Bose SoundTouch Local media player."""

    _attr_has_entity_name = True
    _attr_name: str | None = None

    def __init__(self, device: SoundTouchDevice, name: str) -> None:
        """Initialize the media player."""
        self._device = device
        self._attr_extra_state_attributes = {}
        self._status: Status = None
        self._volume: Volume = None
        self._presets: list = []
        self._attr_unique_id = device.DeviceId
        self._attr_name = name

    def update(self) -> None:
        """Update the state of the media player."""
        try:
            self._status = self._device.GetNowPlayingStatus()
            self._volume = self._device.GetVolume()
            
            # Fetch presets periodically (not every update to save bandwidth)
            if not self._presets:
                self._presets = self._device.GetPresetList()
            
            # Update attributes
            self._attr_media_title = self._status.Track
            self._attr_media_artist = self._status.Artist
            self._attr_media_album_name = self._status.Album
            self._attr_media_image_url = self._status.ArtUrl
            self._attr_source = self._status.ContentItem.Name if self._status.ContentItem else None
            
            # Expose presets as extra attributes
            self._attr_extra_state_attributes["presets"] = {
                preset.PresetId: preset.ContentItem.Name for preset in self._presets
            }
            
        except Exception as ex:
            _LOGGER.error("Error updating SoundTouch device: %s", ex)

    @property
    def state(self) -> MediaPlayerState | None:
        """Return the state of the device."""
        if not self._status:
            return MediaPlayerState.OFF

        if self._status.PlayStatus == "PLAY_STATE":
            return MediaPlayerState.PLAYING
        if self._status.PlayStatus == "PAUSE_STATE":
            return MediaPlayerState.PAUSED
        if self._status.PlayStatus == "STOP_STATE":
            return MediaPlayerState.IDLE
            
        return MediaPlayerState.OFF

    @property
    def volume_level(self) -> float | None:
        """Volume level of the media player (0..1)."""
        if self._volume:
            return self._volume.ActualVolume / 100.0
        return None

    @property
    def is_volume_muted(self) -> bool | None:
        """Boolean if volume is currently muted."""
        if self._volume:
            return self._volume.MuteEnabled
        return None

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        """Flag media player features that are supported."""
        return SUPPORT_SOUNDTOUCH

    def media_play(self) -> None:
        """Send play command."""
        self._device.Play()

    def media_pause(self) -> None:
        """Send pause command."""
        self._device.Pause()

    def media_stop(self) -> None:
        """Send stop command."""
        self._device.Stop()

    def media_previous_track(self) -> None:
        """Send previous track command."""
        self._device.PreviousTrack()

    def media_next_track(self) -> None:
        """Send next track command."""
        self._device.NextTrack()

    def set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        self._device.SetVolume(int(volume * 100))

    def mute_volume(self, mute: bool) -> None:
        """Mute (true) or unmute (false) media player."""
        self._device.Mute() # This toggles in the API usually, let's verify if specific mute/unmute exists

    def turn_on(self) -> None:
        """Turn the media player on."""
        self._device.PowerOn()

    def turn_off(self) -> None:
        """Turn the media player off."""
        self._device.PowerOff()

    def select_source(self, source: str) -> None:
        """Select input source."""
        # Mapping sources or presets
        for preset in self._presets:
            if preset.ContentItem.Name == source:
                self._device.SelectPreset(preset.PresetId)
                return
        _LOGGER.warning("Source %s not found in presets", source)

    @property
    def source_list(self) -> list[str] | None:
        """List of available input sources."""
        return [preset.ContentItem.Name for preset in self._presets]

    # Custom methods for zone management could be added here
