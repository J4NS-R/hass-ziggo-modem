import yaml

from custom_components.ziggo_modem import ModemApi


class TestModemApi:

    def setup_method(self):
        with open('development/secrets.yaml', 'r') as f:
            secrets = yaml.safe_load(f)
        self.modem_api = ModemApi(secrets['default_gateway'], secrets['router_password'])

    def test_api(self):
        devices = self.modem_api.get_connected_devices()
        assert len(devices) > 0
