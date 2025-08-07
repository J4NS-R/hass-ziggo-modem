from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
import logging
import json

from .modem_api import ModemApi

LOGGER = logging.getLogger(__name__)

def setup_platform(hass: HomeAssistant, config: ConfigType, add_entities, discovery_info = None):
    LOGGER.debug('config: %s', json.dumps(config))
    default_gateway = config.get('default_gateway')
    router_password = config.get('router_password')
    if not default_gateway or not router_password:
        raise Exception("Missing default_gateway or router_password properties!")

    modem_api = ModemApi(default_gateway, router_password)

    add_entities([ConnectedDevicesSensor(modem_api)])

class ConnectedDevicesSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, modem_api: ModemApi):
        self._attr_unique_id = "ziggo_modem_connected_devices"
        self._attr_name = "Ziggo Modem Connected Devices"
        self._attr_icon = 'mdi:devices'
        self._attr_device_class = None  # Arbitrary number
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_should_poll = True
        self._attr_available = False
        self.modem_api = modem_api

    def update(self):
        """Update entity state."""
        hosts = self.modem_api.get_connected_devices()
        LOGGER.debug('Found %d hosts', len(hosts))
        LOGGER.debug('%s', hosts)
        self._attr_native_value = len(hosts)
        self._attr_available = True
