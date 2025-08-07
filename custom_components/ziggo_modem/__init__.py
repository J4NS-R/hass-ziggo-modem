"""Ziggo SmartWiFi Modem Integration"""
import voluptuous as vol
from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import load_platform
import logging

from custom_components.ziggo_modem.modem_api import ModemApi

DOMAIN = "ziggo_modem"

CONF_DEFAULT_GATEWAY = 'default_gateway'
CONF_ROUTER_PASSWORD = 'router_password'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_DEFAULT_GATEWAY): str,
        vol.Required(CONF_ROUTER_PASSWORD): str
    })
}, extra=vol.ALLOW_EXTRA)

LOGGER = logging.getLogger(__name__)

def setup(hass: HomeAssistant, config):
    if DOMAIN in config:
        domain_conf = config[DOMAIN]

        hass.data[DOMAIN] = {
            'config': domain_conf,
            'modem_api': ModemApi(domain_conf[CONF_DEFAULT_GATEWAY], domain_conf[CONF_ROUTER_PASSWORD])
        }
        return True
    else:
        LOGGER.error('%s key is not in configuration.yaml', DOMAIN)
        return False
