"""Tests for the KEBA charging station sensors."""

from typing import Any
from unittest.mock import MagicMock

from freezegun.api import FrozenDateTimeFactory
import pytest
from syrupy.assertion import SnapshotAssertion

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from . import snapshot_keba_platform
from .conftest import async_advance


async def test_sensors(
    hass: HomeAssistant,
    setup_keba: MagicMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the sensor entities, their unique IDs and states."""
    snapshot_keba_platform(hass, entity_registry, snapshot, Platform.SENSOR)


@pytest.mark.parametrize("keba_fixture", ["p30_plugged.json", "p30_charging.json"])
async def test_sensor_states(
    hass: HomeAssistant, setup_keba: MagicMock, snapshot: SnapshotAssertion
) -> None:
    """Test the sensor states with a car plugged in, and with a car charging."""
    states = sorted(
        hass.states.async_all(Platform.SENSOR), key=lambda state: state.entity_id
    )
    assert len(states) == 5
    assert states == snapshot


async def test_sensors_follow_the_station(
    hass: HomeAssistant,
    setup_keba: MagicMock,
    keba_data: dict[str, Any],
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test a poll carries new values from the library into the sensors."""
    keba_data.update({"Curr user": 10.0, "Setenergy": 20.0, "P": 3.6})
    keba_data["E total"] = 12350.0

    await async_advance(hass, freezer, 5)

    assert hass.states.get("sensor.keba_p30_max_current").state == "10.0"
    assert hass.states.get("sensor.keba_p30_energy_target").state == "20.0"
    assert hass.states.get("sensor.keba_p30_charging_power").state == "3.6"
    assert hass.states.get("sensor.keba_p30_total_energy").state == "12350.0"
