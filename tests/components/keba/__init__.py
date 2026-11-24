"""Tests for the KEBA charging station integration."""

from syrupy.assertion import SnapshotAssertion

from homeassistant.components.keba.const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er


def snapshot_keba_platform(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    domain: str,
) -> None:
    """Snapshot the registry entries and states of one KEBA platform."""
    # snapshot_platform finds entities by config entry; a YAML setup has none.
    entries = sorted(
        (
            entry
            for entry in entity_registry.entities.values()
            if entry.platform == DOMAIN and entry.domain == domain
        ),
        key=lambda entry: entry.entity_id,
    )
    assert entries
    for entry in entries:
        assert entry == snapshot(name=f"{entry.entity_id}-entry")
        assert hass.states.get(entry.entity_id) == snapshot(
            name=f"{entry.entity_id}-state"
        )
