"""Platform for sensor integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import InvalidStateError
from homeassistant.helpers import entity_platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.chore.chore_counter import CounterChore
from custom_components.chore.chore_scheduled import ScheduledChore
from custom_components.chore.const import SCHEDULED_CHORE, COUNTER_CHORE, CounterFeatures

_LOG = logging.getLogger(__name__)

ENTITY_FACTORY = {
    SCHEDULED_CHORE: ScheduledChore.from_config_entry,
    COUNTER_CHORE: CounterChore.from_config_entry,
}

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """register entities for new configs created via 'Helpers'"""

    _LOG.debug('creating entity for a new config %s', config_entry.title)
    _LOG.debug('options %s', config_entry.options)

    chore_type = config_entry.options.get('chore_type', '')

    factory_function = ENTITY_FACTORY.get(chore_type, None)
    if factory_function is None:
        raise InvalidStateError(f'Unsupported chore type {chore_type} in {config_entry.entry_id}({config_entry.title})')

    entity = factory_function(config_entry)
    async_add_entities([entity])
    _LOG.debug('Added entity %s (%s) for config entry {config_entry.entry_id} to HA', entity.entity_id, entity.name)

    _register_services()

def _register_services():
    platform = entity_platform.async_get_current_platform()

    platform.async_register_entity_service(
        'increment',
        {
            'increment': int
        },
        'increment',
        required_features=[
            CounterFeatures.INCREMENT
        ]
    )

    platform.async_register_entity_service(
        'complete',
        {
            'reset_from_today': bool
        },
        'complete',
    )

    platform.async_register_entity_service(
        'set_counter',
        {
            'counter_state': int
        },
        'set_counter',
        required_features=[
            CounterFeatures.INCREMENT
        ]
    )

