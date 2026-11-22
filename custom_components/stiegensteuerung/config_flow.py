"""Set up the bundled blueprint distribution through the UI."""
from homeassistant import config_entries

class SetupFlow(config_entries.ConfigFlow, domain="stiegensteuerung"):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        await self.async_set_unique_id("stiegensteuerung")
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title="Stiegensteuerung", data={})
