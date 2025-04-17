import logging
from datetime import datetime, date, timedelta

from dateutil.relativedelta import relativedelta
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityPlatformState

from custom_components.chore.const import WEEK, DAY, SUPPORTED_STATES, STATE_OVERDUE, STATE_SOON, STATE_UPCOMING, MONTH, DUE_SOON_DAYS
from custom_components.chore.utils import filter_kwargs_for_init

_LOG = logging.getLogger(__name__)

class ScheduledChore(SensorEntity):
    """Sensor to notify whether chore is due/past based on current date"""

    @classmethod
    def from_config_entry(cls, config_entry: ConfigEntry):
        start_from = config_entry.options.get('start_from', datetime.today().date().isoformat())

        return ScheduledChore(
            unique_id=config_entry.entry_id,
            start_from=date.fromisoformat(start_from),
            **filter_kwargs_for_init(ScheduledChore, config_entry.options, skip_additionally=['start_from'])
        )

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = SUPPORTED_STATES

    _attr_icon = 'mdi:broom'

    def __init__(self, name: str, period: int, schedule_type: str, start_from: date, unique_id: str):
        super().__init__()
        self._attr_name = name
        self._period = period
        self._schedule_type = schedule_type
        self._start_from = start_from
        self._attr_unique_id = unique_id
        self._next_due_date = None

        self.reset(start_from)

    def _calculate_next_due_date(self, start_from: date) -> date:

        if self._schedule_type == DAY:
            return start_from + timedelta(days=self._period)
        elif self._schedule_type == WEEK:
            return start_from + timedelta(weeks=self._period)
        elif self._schedule_type == MONTH:
            return start_from + relativedelta(months=self._period)
        else:
            raise ValueError(f'Unsupported schedule type: {self._schedule_type}')

    @property
    def extra_state_attributes(self):
        return {
            'chore_integration': True,
            'period': self._period,
            'schedule_type': self._schedule_type,
            'start_from': self._start_from,
            'next_due_date': self._next_due_date,
        }

    def update(self) -> None:
        """
        Calculate state based on due date
        """
        current_date = date.today()
        self._attr_native_value = (
            STATE_OVERDUE
           if current_date >= self._next_due_date
           else STATE_SOON if (self._next_due_date - current_date).days <= DUE_SOON_DAYS
           else STATE_UPCOMING
        )

    def reset(self, start_from: date = date.today()):
        """calculate next due date"""

        self._next_due_date = self._calculate_next_due_date(start_from)
        self.update()

        _LOG.debug('Reset entity %s to the next due date %s. Updated state to %s', self.entity_id, self._next_due_date.isoformat(), self._attr_native_value)

        if self._platform_state == EntityPlatformState.ADDED:
            self.async_write_ha_state()
