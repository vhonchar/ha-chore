import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from custom_components.chore.chore_countdown import CountdownChore
from custom_components.chore.chore_scheduled import ScheduledChore
from custom_components.chore.const import DOMAIN, PLATFORMS, CountdownFeatures

LOG = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up platform - register services, initialize data structure."""

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hello World from a config entry."""

    entry.async_on_unload(entry.add_update_listener(update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    LOG.warning(f'entry {entry.entry_id} ({entry.title}) is updated. Should I do something?')

    await hass.config_entries.async_forward_entry_unload(entry, Platform.SENSOR)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
