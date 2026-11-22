"""Install bundled Home Assistant blueprints, preserving instance inputs."""
import logging
from pathlib import Path

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

BLUEPRINTS = (("automation","lichtuebernahme","stiegensteuerung-lichtuebernahme"),("automation","ausfallerkennung","stiegensteuerung-ausfallerkennung"))


def _install(root: Path) -> set[str]:
    changed = set()
    bundle = Path(__file__).parent / "blueprints"
    for domain, source, name in BLUEPRINTS:
        data = (bundle / domain / f"{source}.yaml").read_bytes()
        target = root / "blueprints" / domain / "oniel10" / f"{name}.yaml"
        if target.exists():
            previous = target.read_bytes()
            if previous == data:
                continue
            if source == "lichtuebernahme" and any(
                marker in previous for marker in (b"switch_kg_", b"light_kg_")
            ):
                _LOGGER.warning("Stair blueprint uses legacy inputs; migrate its instance before replacing the file")
                continue
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(".yaml.tmp")
        temporary.write_bytes(data)
        temporary.replace(target)
        changed.add(domain)
    return changed


async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    """Update bundled files after starting Home Assistant."""
    async def install(_event=None):
        changed = await hass.async_add_executor_job(_install, Path(hass.config.config_dir))
        for domain in changed:
            if hass.services.has_service(domain, "reload"):
                await hass.services.async_call(domain, "reload", blocking=True)

    if hass.is_running:
        await install()
    else:
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, install)
    return True
