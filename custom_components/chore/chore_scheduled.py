from random import randint
from datetime import datetime

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry

from custom_components.chore.const import DEFAULT_SCHEDULE_TYPE


def to_date(date_as_string: str):
    return datetime.strptime(date_as_string, '%Y-%m-%d')

class ScheduledChore(SensorEntity):
    """Sensor to notify when scheduled chore is due/past"""

    @classmethod
    def from_config_entry(cls, config_entry: ConfigEntry):
        start_from = config_entry.options.get('start_from', datetime.today().date().isoformat())

        return ScheduledChore(
            config_entry.title,
            period=config_entry.options.get('period', 1),
            schedule_type=config_entry.options.get('schedule_type', DEFAULT_SCHEDULE_TYPE),
            start_from=to_date(start_from),
            unique_id=config_entry.entry_id,
        )

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = [
        'past',
        'due_soon',
        'good'
    ]

    _attr_icon = 'mdi:broom'

    def __init__(self, name, period, schedule_type, start_from, unique_id):
        super().__init__()
        self._attr_name = name
        self._period = period
        self._schedule_type = schedule_type
        self._start_from = start_from
        self._attr_unique_id = unique_id

    def update(self) -> None:
        """
        Calculate state based on due date
        """
        self._attr_native_value = 'good' if randint(0, 1) == 0 else 'past'

    @property
    def extra_state_attributes(self):
        return {
            'period': self._period,
            'schedule_type': self._schedule_type,
            'start_from': self._start_from,
        }
