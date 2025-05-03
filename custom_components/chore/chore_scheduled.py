import logging
from datetime import date, timedelta
from typing import override

from dateutil.relativedelta import relativedelta
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityPlatformState
from homeassistant.helpers.restore_state import RestoreEntity

from custom_components.chore.const import WEEK, DAY, SUPPORTED_STATES, STATE_OVERDUE, STATE_SOON, STATE_UPCOMING, MONTH, DUE_SOON_DAYS
from custom_components.chore.utils import filter_kwargs_for_init, ha_today

_LOG = logging.getLogger(__name__)

class ScheduledChore(SensorEntity, RestoreEntity):
    """Sensor to notify whether chore is due/past based on current date"""

    @classmethod
    def from_config_entry(cls, hass: HomeAssistant, config_entry: ConfigEntry):

        start_from = config_entry.options.get('start_from', ha_today(hass).isoformat())

        start_from = date.fromisoformat(start_from)
        _LOG.debug(f'start from date is {start_from}')

        return ScheduledChore(
            unique_id=config_entry.entry_id,
            hass=hass,
            start_from=start_from,
            **filter_kwargs_for_init(ScheduledChore, config_entry.options, skip_additionally=['start_from'])
        )

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = SUPPORTED_STATES

    _attr_icon = 'mdi:broom'

    def __init__(self, hass: HomeAssistant, name: str, interval: int, interval_unit: str, start_from: date, unique_id: str):
        super().__init__()
        self.hass = hass
        self._attr_name = name
        self._interval = interval
        self._interval_unit = interval_unit
        self._attr_unique_id = unique_id
        self._next_due_date = None
        self._last_completion_date = start_from

        self._set_next_due_date(start_from)

    @override
    async def async_added_to_hass(self) -> None:
        """When sensor is added to HA, restore state and add it to calendar."""
        await super().async_added_to_hass()

        # Restore stored state
        if (last_state := await self.async_get_last_state()) is not None:
            _LOG.debug(f'found previous state of counter chore {self.entity_id}')

            last_completion_date = last_state.attributes.get('last_completion_date')
            self._last_completion_date = date.fromisoformat(last_completion_date) if last_completion_date is not None else self._last_completion_date

            next_due_date = last_state.attributes.get('next_due_date')
            self._next_due_date = date.fromisoformat(next_due_date) if next_due_date is not None else self._next_due_date

            self.update()

    @property
    def extra_state_attributes(self):
        return {
            'chore_integration': True,
            'interval': self._interval,
            'interval_unit': self._interval_unit,
            'next_due_date': self._next_due_date.isoformat(),
            'last_completion_date': self._last_completion_date.isoformat(),
        }

    def update(self) -> None:
        """
        Calculate state based on due date
        """
        current_date = ha_today(self.hass)
        self._attr_native_value = (
            STATE_OVERDUE
           if current_date >= self._next_due_date
           else STATE_SOON if (self._next_due_date - current_date).days <= DUE_SOON_DAYS
           else STATE_UPCOMING
        )

    def _set_next_due_date(self, starting_from: date):
        """calculate next due date"""

        self._next_due_date = self._calculate_next_due_date(starting_from)
        while self._next_due_date < ha_today(self.hass):
            self._next_due_date = self._calculate_next_due_date(self._next_due_date)

        self.update()

        _LOG.debug('Reset entity %s to the next due date %s. Updated state to %s', self.entity_id, self._next_due_date.isoformat(), self._attr_native_value)

        if self._platform_state == EntityPlatformState.ADDED:
            self.async_write_ha_state()

    def _calculate_next_due_date(self, start_from: date) -> date:

        if self._interval_unit == DAY:
            return start_from + timedelta(days=self._interval)
        elif self._interval_unit == WEEK:
            return start_from + timedelta(weeks=self._interval)
        elif self._interval_unit == MONTH:
            return start_from + relativedelta(months=self._interval)
        else:
            raise ValueError(f'Unsupported schedule type: {self._interval_unit}')

    async def complete(self, reset_from_today: bool):
        today = ha_today(self.hass)
        _LOG.debug(f'today is {today}')
        self._last_completion_date = today
        self._set_next_due_date(today if reset_from_today else self._next_due_date)
