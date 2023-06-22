import os

import requests


class Hydrawise:
    def __init__(self):
        self.API_LOCATION = 'https://api.hydrawise.com/api/v1'
        self.API_KEY = os.environ.get('HYDRAWISE_API_KEY')
        self.zone_map = self._build_zone_map()

    def _request(self, path: str, params: dict) -> dict:
        params['api_key'] = self.API_KEY
        res = {}
        try:
            res = requests.get(self.API_LOCATION + path, params=params).json()
        except Exception as e:
            raise e
        return res

    def _build_zone_map(self):
        relay_map = {}
        schedules = self.get_schedules()
        for relay in schedules['relays']:
            relay_map[str(relay['relay'])] = relay['relay_id']
        return relay_map

    def get_schedules(self, controller_id: int = 0) -> dict:
        path = '/statusschedule.php'
        params = dict()
        if controller_id:
            params['controller_id'] = controller_id
        return self._request(path, params)

    def get_customer_details(self) -> dict:
        path = '/customerdetails.php'
        params = dict()
        return self._request(path, params)

    def run_zone(self, zone_id: str, run_time: int = 60) -> dict:
        path = '/setzone.php'
        params = dict(action='run', custom=run_time, relay_id=self.zone_map[zone_id])
        return self._request(path, params)

    def stop_zone(self, zone_id: str) -> dict:
        path = '/setzone.php'
        params = dict(action='stop', relay_id=self.zone_map[zone_id])
        return self._request(path, params)
