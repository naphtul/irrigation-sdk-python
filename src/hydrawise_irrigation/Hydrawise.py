import os

import requests


class Hydrawise:
    def __init__(self, api_key: str = ''):
        self.API_LOCATION = 'https://api.hydrawise.com/api/v1'
        self.api_key = api_key if api_key else os.environ.get('HYDRAWISE_API_KEY')
        self.zone_map = self._build_zone_map()

    def _request(self, path: str, params: dict) -> dict:
        if not self.api_key:
            raise ValueError('API Key param not properly defined.')
        params['api_key'] = self.api_key
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


if __name__ == '__main__':
    hydrawise = Hydrawise('')
    print(hydrawise.get_customer_details())
