"""Utility functions."""
import inspect
from datetime import date, datetime
from typing import Any
from zoneinfo import ZoneInfo

from homeassistant.core import HomeAssistant


def filter_kwargs_for_init(cls: type, kwargs: dict[str, Any], skip_additionally: list[str] = ()) -> dict[str, Any]:
    """Filter provided dictionary to leave only those keys, which are met in constructor of the cls."""
    sig = inspect.signature(cls.__init__)
    valid_params = set(sig.parameters) - {"self"}
    return {k: v for k, v in kwargs.items() if k in valid_params and k not in skip_additionally}

def ha_today(hass: HomeAssistant) -> date:
    """Get today's date in time zone configured in HomeAssistant."""
    ha_tz = ZoneInfo(hass.config.time_zone)
    return datetime.now(ha_tz).date()
