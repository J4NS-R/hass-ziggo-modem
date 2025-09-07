from typing import override
import logging
import requests

LOGGER = logging.getLogger(__name__)

class ModemApiSession(requests.Session):
    def __init__(self, router_password, login_url):
        super().__init__()
        self._router_password = router_password
        self._login_url = login_url
        self.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'HomeAssistant/ziggo_modem',
            'Authorization': 'Bearer bad_token'
        })
        self.verify = False

    def _refresh_token(self):
        resp = requests.post(self._login_url, json={'password': self._router_password}, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'HomeAssistant/ziggo_modem',
        })
        resp.raise_for_status()
        new_token = resp.json()['created']['token']
        self.headers.update({'Authorization': f'Bearer {new_token}'})
        LOGGER.debug('Successfully refreshed auth token')

    @override
    def request(self, *args, **kwargs):
        resp = super().request(*args, **kwargs)
        if resp.status_code in {401, 403}:
            self._refresh_token()
            resp = super().request(*args, **kwargs)
        resp.raise_for_status()
        return resp

class ModemApi:
    def __init__(self, default_gateway: str, router_password: str):
        self.api_base_url = f'https://{default_gateway}/rest/v1'
        self.session = ModemApiSession(router_password, self.api_base_url+'/user/login')
        LOGGER.debug('Configured ModemAPI with base URL: %s', self.api_base_url)

    def get_connected_devices(self):
        """Get list of connected devices."""
        response = self.session.get(
            self.api_base_url + '/network/hosts?connectedOnly=true',
        )
        response.raise_for_status()

        return response.json()['hosts']['hosts']
