from pprint import pprint

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
import requests
import logging
import json

LOGGER = logging.getLogger(__name__)

def setup_platform(hass: HomeAssistant, config: ConfigType, add_entities, discovery_info = None):
    LOGGER.debug('config: %s', json.dumps(config))
    default_gateway = config.get('default_gateway')
    router_password = config.get('router_password')
    if not default_gateway or not router_password:
        raise Exception("Missing default_gateway or router_password properties!")
    add_entities([ConnectedDevicesSensor(default_gateway, router_password)])

class ConnectedDevicesSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, default_gateway, router_password):
        self._attr_unique_id = "ziggo_modem_connected_devices"
        self._attr_name = "Ziggo Modem Connected Devices"
        self._attr_icon = 'mdi:devices'
        self._attr_device_class = None  # Arbitrary number
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_should_poll = True
        self.api_base_url = f'http://{default_gateway}/rest/v1'
        self.router_password = router_password

    def update(self):
        """Update entity state."""
        common_headers = {
            'Accept': 'application/json',
            'User-Agent': 'Python/requests',
        }
        res = requests.post(self.api_base_url + '/user/login', json={'password': self.router_password}, headers={
            'Content-Type': 'application/json',
            **common_headers
        })
        res.raise_for_status()

        auth_token = res.json()['created']['token']
        auth_header = {'Authorization': f'Bearer {auth_token}'}

        res = requests.get(self.api_base_url + '/network/hosts?connectedOnly=true', headers=auth_header)
        res.raise_for_status()
        hosts = res.json()['hosts']['hosts']
        LOGGER.debug('hosts: %s', json.dumps(hosts))

        self._attr_native_value = len(hosts)
