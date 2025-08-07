# Home Assistant Ziggo SmartWiFi Modem Integration

Provides a sensor with the current number of devices connected to your router.

## Installation

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=J4NS-R&repository=hass-ziggo-modem&category=integration)

```yaml
# configuration.yaml

ziggo_modem:
  default_gateway: 192.168.178.1
  router_password: examplePassword

sensor:
  - platform: ziggo_modem
```

## Development

1. Put secrets in `development/secrets.yaml`
2. `docker compose up -d`
