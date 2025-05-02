from enum import IntFlag

from homeassistant.const import Platform

DOMAIN = 'chore'
PLATFORMS = [Platform.SENSOR]

# types of chores
SCHEDULED_CHORE = 'scheduled'
COUNTER_CHORE = 'counter'

# schedule units
DAY='DAY'
WEEK='WEEK'
MONTH='MONTH'

DEFAULT_SCHEDULE_TYPE=DAY

# sensor states
STATE_UPCOMING='upcoming'   # scheduled and upcoming in some time
STATE_SOON='soon'           # due in couple days/cycles
STATE_OVERDUE='overdue'     # overdue

SUPPORTED_STATES = [
    STATE_UPCOMING,
    STATE_SOON,
    STATE_OVERDUE,
]

# amount of days before next due date to mark a chore as "soon"
DUE_SOON_DAYS = 2

# features
class CounterFeatures(IntFlag):
    """Supported features of the counter chore entity."""

    INCREMENT = 1
