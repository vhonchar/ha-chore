"""Platform for sensor integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.chore.chore_countdown import CountdownChore
from custom_components.chore.chore_scheduled import ScheduledChore
from custom_components.chore.const import SCHEDULED_CHORE, COUNTDOWN_CHORE

LOG = logging.getLogger(__name__)

ENTITY_FACTORY = {
    SCHEDULED_CHORE: ScheduledChore.from_config_entry,
    COUNTDOWN_CHORE: CountdownChore.from_config_entry,
}

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    LOG.warning(f'creating entity for a new config {config_entry.title}')
    LOG.warning(f'data {config_entry.data}')
    LOG.warning(f'options {config_entry.options}')

    chore_type = config_entry.options.get('chore_type', '')

    if ENTITY_FACTORY.get(chore_type, None) is not None:
        entity = ENTITY_FACTORY[chore_type](config_entry=config_entry)
        async_add_entities([entity])

        LOG.warning(f'Added entity {entity.entity_id} ({entity.name}) for config entry {config_entry.entry_id} to HA')
    else:
        raise ValueError(f'Unsupported chore type {chore_type} in {config_entry.entry_id}({config_entry.title})')
