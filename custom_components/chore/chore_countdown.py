from datetime import datetime

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry

from custom_components.chore.const import CountdownFeatures

def to_date(date_as_string: str):
    return datetime.strptime(date_as_string, '%Y-%m-%d')

class CountdownChore(SensorEntity):
    """Sensor to notify when a chore is due based on a countdown"""

    @classmethod
    def from_config_entry(cls, config_entry: ConfigEntry):
        return CountdownChore(
            config_entry.title,
            limit=config_entry.options.get('limit', 1),
            unique_id=config_entry.entry_id,
        )

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = [
        'past',
        'due_soon',
        'good'
    ]
    _attr_icon = 'mdi:broom'
    _attr_should_poll = False
    _attr_supported_features = CountdownFeatures.INCREMENT

    def __init__(self, name, limit, unique_id):
        super().__init__()
        self._attr_name = name
        self._limit = limit
        self._counter_state = limit
        self._calculate_state()
        self._attr_unique_id = unique_id

    @property
    def extra_state_attributes(self):
        return {
            'counter_state': self._counter_state,
            'limit': self._limit
        }

    async def increment(self, increment: int):
        """Increment current state by provided value"""
        self._counter_state -= increment
        self._calculate_state()
        self.async_write_ha_state()

    def _calculate_state(self):
        self._attr_native_value = 'past' if self._counter_state <= 0 else 'due_soon' if self._counter_state <= 2 else 'good'
