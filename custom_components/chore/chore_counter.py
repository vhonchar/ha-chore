from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry

from custom_components.chore import const
from custom_components.chore.const import CounterFeatures, SUPPORTED_STATES
from custom_components.chore.utils import filter_kwargs_for_init

class CounterChore(SensorEntity):
    """Sensor to notify when a chore is due based on a counter"""

    @classmethod
    def from_config_entry(cls, config_entry: ConfigEntry):
        return CounterChore(
            unique_id=config_entry.entry_id,
            **filter_kwargs_for_init(CounterChore, config_entry.options)
        )

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = SUPPORTED_STATES
    _attr_should_poll = False
    _attr_supported_features = CounterFeatures.INCREMENT
    _attr_icon = 'mdi:broom'

    def __init__(self, name, limit, unique_id):
        super().__init__()
        self._attr_name = name
        self._limit = limit
        self._counter_state = 0
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
        self._counter_state += increment
        self._calculate_state()
        self.async_write_ha_state()

    def _calculate_state(self):
        self._attr_native_value = (
            const.STATE_OVERDUE if self._counter_state >= self._limit
            else const.STATE_SOON if self._limit - self._counter_state <= 2
            else const.STATE_UPCOMING
        )
