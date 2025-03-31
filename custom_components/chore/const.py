from homeassistant.const import Platform

DOMAIN = 'chore'
PLATFORMS = [Platform.SENSOR]

# types of chores
SCHEDULED_CHORE = 'scheduled'
COUNTDOWN_CHORE = 'countdown'

# types of scheduled chores
DAY='DAY'
WEEK='WEEK'
MONTH='MONTH'

DEFAULT_SCHEDULE_TYPE=DAY
