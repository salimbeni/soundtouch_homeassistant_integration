"""Favorites manager for SoundTouchLocal integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.storage import Store

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STORAGE_KEY = f"{DOMAIN}.favorites"
STORAGE_VERSION = 1

class SoundTouchFavorite:
    """Class to represent a SoundTouch favorite."""

    def __init__(
        self,
        name: str,
        source: str,
        item_type: str,
        location: str,
        source_account: str | None = None,
        container_art: str | None = None,
        is_presetable: bool = True,
    ) -> None:
        """Initialize a new SoundTouch favorite."""
        self.name = name
        self.source = source
        self.item_type = item_type
        self.location = location
        self.source_account = source_account
        self.container_art = container_art
        self.is_presetable = is_presetable

    def to_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the favorite."""
        return {
            "name": self.name,
            "source": self.source,
            "item_type": self.item_type,
            "location": self.location,
            "source_account": self.source_account,
            "container_art": self.container_art,
            "is_presetable": self.is_presetable,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SoundTouchFavorite:
        """Create a SoundTouch favorite from a dictionary."""
        return cls(
            name=data["name"],
            source=data["source"],
            item_type=data["item_type"],
            location=data["location"],
            source_account=data.get("source_account"),
            container_art=data.get("container_art"),
            is_presetable=data.get("is_presetable", True),
        )


class FavoritesManager:
    """Class to manage local favorites for SoundTouch devices."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the favorites manager."""
        self.hass = hass
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._favorites: list[SoundTouchFavorite] = []

    async def async_load(self) -> None:
        """Load favorites from storage."""
        data = await self._store.async_load()
        if data:
            self._favorites = [SoundTouchFavorite.from_dict(f) for f in data.get("favorites", [])]
        else:
            self._favorites = []

    async def async_save(self) -> None:
        """Save favorites to storage."""
        await self._store.async_save({
            "favorites": [f.to_dict() for f in self._favorites]
        })

    @callback
    def get_favorites(self) -> list[SoundTouchFavorite]:
        """Return the list of favorites."""
        return self._favorites

    async def async_add_favorite(self, favorite: SoundTouchFavorite) -> None:
        """Add a favorite to the list and save."""
        # Check if already exists (by location and source)
        for f in self._favorites:
            if f.location == favorite.location and f.source == favorite.source:
                return # Already exists
        
        self._favorites.append(favorite)
        await self.async_save()

    async def async_remove_favorite(self, location: str) -> None:
        """Remove a favorite by location and save."""
        self._favorites = [f for f in self._favorites if f.location != location]
        await self.async_save()
