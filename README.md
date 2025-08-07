# Home Assistant Ziggo SmartWiFi Modem Integration

Provides a sensor with the current number of devices connected to your router.

## Installation

(HACS integration WIP)

```yaml
# configuration.yaml

sensor:
  - platform: ziggo_modem
    default_gateway: 192.168.178.1
    router_password: examplePassword
```

## Development

1. Put secrets in `development/secrets.yaml`
2. `docker compose up -d`
