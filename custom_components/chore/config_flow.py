import logging
from typing import Any, cast, Coroutine, Callable

import voluptuous as vol
from datetime import date
from homeassistant.core import callback
from homeassistant.helpers.schema_config_entry_flow import SchemaConfigFlowHandler, SchemaFlowFormStep, SchemaFlowMenuStep, SchemaCommonFlowHandler
from homeassistant.helpers import selector

from custom_components.chore import const

LOGGER = logging.getLogger(__name__)

async def choose_options_step(options: dict[str, Any]) -> str:
    """Return next step_id for options flow according to group_type."""
    return cast(str, options.get('chore_type', options.get('type', '')))

def set_chore_type(chore_type: str) -> Callable[[SchemaCommonFlowHandler, dict[str, Any]], Coroutine[Any, Any, dict[str, Any]]]:
    """Set chore type."""
    async def _set_chore_type(_: SchemaCommonFlowHandler, user_input: dict[str, Any]) -> dict[str, Any]:
        """Add chore type to user input."""
        return dict(chore_type=chore_type, **user_input)
    return _set_chore_type

BASIC_SCHEMA = vol.Schema({
    vol.Required('name'): selector.TextSelector(),
})

SCHEDULED_CHORE_SCHEMA = vol.Schema({
    vol.Required('interval', default=1): vol.All(
            selector.NumberSelector(selector.NumberSelectorConfig(
            min=1,
            mode=selector.NumberSelectorMode.BOX,
            step=1,
        )),
        vol.Coerce(int)
    ),
    vol.Required('interval_unit'): selector.SelectSelector(selector.SelectSelectorConfig(
        options=[const.DAY, const.WEEK, const.MONTH],
        mode=selector.SelectSelectorMode.DROPDOWN
    )),
    vol.Required('start_from', default=date.today().isoformat()): selector.DateSelector(),
})

COUNTER_CHORE_SCHEMA = vol.Schema({
    vol.Required('limit', default=10): selector.NumberSelector(selector.NumberSelectorConfig(
        min=1,
        mode=selector.NumberSelectorMode.BOX,
        step=1,
    )),
})

CONFIG_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    'user': SchemaFlowMenuStep([const.SCHEDULED_CHORE, const.COUNTER_CHORE]),
    const.SCHEDULED_CHORE: SchemaFlowFormStep(
        BASIC_SCHEMA.extend(SCHEDULED_CHORE_SCHEMA.schema),
        validate_user_input=set_chore_type(const.SCHEDULED_CHORE)
    ),
    const.COUNTER_CHORE: SchemaFlowFormStep(
        BASIC_SCHEMA.extend(COUNTER_CHORE_SCHEMA.schema),
        validate_user_input=set_chore_type(const.COUNTER_CHORE)
    ),
}

OPTIONS_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    'init': SchemaFlowFormStep(next_step=choose_options_step),
    const.SCHEDULED_CHORE: SchemaFlowFormStep(SCHEDULED_CHORE_SCHEMA),
    const.COUNTER_CHORE: SchemaFlowFormStep(COUNTER_CHORE_SCHEMA),
}

class ChoreHelperConfigFlowHandler(SchemaConfigFlowHandler, domain=const.DOMAIN):
    """Handle a config or options flow for Chore Helper."""

    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW
    VERSION = 1

    @callback
    def async_config_entry_title(self, options: dict[str, Any]) -> str:
        """Return config entry title.

        The options parameter contains config entry options, which is the union of user
        input from the config flow steps.
        """
        return cast(str, options["name"]) if "name" in options else ""
