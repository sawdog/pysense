from datetime import datetime
import json

import requests
from requests.exceptions import ReadTimeout

from websocket import create_connection
from websocket._exceptions import WebSocketTimeoutException

from pysense import config

API_URL = config.sense.api.url
API_TIMEOUT = config.sense.api.timeout
REALTIME_URL = config.sense.realtime.url
WSS_TIMEOUT = config.websocket.timeout
USERNAME = config.sense.username
PASSWORD = config.sense.password

# for the last hour, day, week, month, or year
valid_scales = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']


class SenseAPITimeoutException(Exception):
    pass


class SenseMonitor(object):

    __username__ = None
    __password__ = None
    _realtime_ = None
    _devices_ = None
    _trend_data_ = None

    def __init__(self, username=None,
                 password=None,
                 api_timeout=API_TIMEOUT,
                 wss_timeout=WSS_TIMEOUT):
        if username is None:
            username = USERNAME
        if password is None:
            password = PASSWORD
        auth_data = {
            "email": username,
            "password": password
        }

        # Timeout instance variables
        self.api_timeout = api_timeout
        self.wss_timeout = wss_timeout

        # Create session
        self.s = requests.session()
        self._trend_data_ = {}
        for scale in valid_scales:
            self._trend_data_[scale] = {}

        # Get auth token
        try:
            response = self.s.post(API_URL+'authenticate',
                                   auth_data,
                                   timeout=self.api_timeout)
        except Exception as e:
            raise Exception('Connection failure: %s' % e)

        # check for 200 return
        if response.status_code != 200:
            raise Exception("Please check username and password."
                            " API Return Code: %s" % response.status_code)

        # Build out some common variables
        json = response.json()
        self.sense_access_token = json['access_token']
        self.account_id = json['account_id']
        self.user_id = json['user_id']
        self.monitor_id = json['monitors'][0]['id']
        self.monitor = json['monitors'][0]
        self.date_created = json['date_created']

        # create the auth header
        self.headers = {'Authorization': 'bearer {}'
                        .format(self.sense_access_token)}

    @property
    def devices(self):
        """Return devices."""
        if self._devices_ is None:
            self._devices_ = self.get_discovered_device_names()

        return self._devices_

    def get_realtime(self):
        try:
            ws = create_connection(REALTIME_URL % (self.monitor_id,
                                                   self.sense_access_token),
                                   timeout=self.wss_timeout)

            for i in range(5):  # hello, features, [updates,] data
                result = json.loads(ws.recv())
                if result.get('type') == 'realtime_update':
                    self._realtime_ = result['payload']
                    return self._realtime_
        except WebSocketTimeoutException:
            raise SenseAPITimeoutException("API websocket timed out")
        finally:
            if ws:
                ws.close()

    def api_call(self, url, payload=None):
        if payload is None:
            payload = {}
        try:
            return self.s.get(API_URL + url,
                              headers=self.headers,
                              timeout=self.api_timeout,
                              data=payload)
        except ReadTimeout:
            raise SenseAPITimeoutException("API call timed out")

    @property
    def realtime(self):
        if not self._realtime_:
            return self.get_realtime()
        return self._realtime_

    @property
    def active_power(self):
        if not self.realtime:
            self.get_realtime()
        return self.realtime.get('w', 0)

    @property
    def active_solar_power(self):
        if not self.realtime:
            self.get_realtime()
        return self.realtime.get('solar_w', 0)

    @property
    def active_voltage(self):
        if not self.realtime:
            self.get_realtime()
        return self.realtime.get('voltage', 0)
    
    @property
    def active_frequency(self):
        if not self.realtime:
            self.get_realtime()
        return self.realtime.get('hz', 0)
    
    @property
    def daily_usage(self):
        return self.get_trend('DAY', False)

    @property
    def daily_production(self):
        return self.get_trend('DAY', True)
    
    @property
    def weekly_usage(self):
        # Add today's usage
        return self.get_trend('WEEK', False)

    @property
    def weekly_production(self):
        # Add today's production
        return self.get_trend('WEEK', True)
    
    @property
    def monthly_usage(self):
        # Add today's usage
        return self.get_trend('MONTH', False)

    @property
    def monthly_production(self):
        # Add today's production
        return self.get_trend('MONTH', True)
    
    @property
    def yearly_usage(self):
        # Add this month's usage
        return self.get_trend('YEAR', False)

    @property
    def yearly_production(self):
        # Add this month's production
        return self.get_trend('YEAR', True)

    @property
    def active_devices(self):
        if not self.realtime:
            self.get_realtime()
        return [d['name'] for d in self.realtime.get('devices', {})]

    def get_trend(self, scale, is_production):
        key = "production" if is_production else "consumption"
        if not self._trend_data_[scale]:
            self.get_trend_data(scale)
        if key not in self._trend_data_[scale]:
            return 0
        total = self._trend_data_[scale][key].get('total', 0)
        if scale == 'WEEK' or scale == 'MONTH':
            return total + self.get_trend('DAY', is_production)
        if scale == 'YEAR':
            return total + self.get_trend('MONTH', is_production)
        return total

    def get_discovered_device_names(self):
        # lots more info in here to be parsed out
        response = self.api_call('app/monitors/%s/devices' %
                                 self.monitor_id)
        self._devices_ = [entry['name'] for entry in response.json()]
        return self._devices_

    def get_discovered_device_data(self):
        response = self.api_call('monitors/%s/devices' %
                                 self.monitor_id)
        return response.json()

    def always_on_info(self):
        # Always on info - pretty generic similar to the web page
        response = self.api_call('app/monitors/%s/devices/always_on' %
                                 self.monitor_id)
        return response.json()

    def get_monitor_info(self):
        # View info on your monitor & device detection status
        response = self.api_call('app/monitors/%s/status' %
                                 self.monitor_id)
        return response.json()

    def get_device_info(self, device_id):
        # Get specific information about a device
        response = self.api_call('app/monitors/%s/devices/%s' %
                                 (self.monitor_id, device_id))
        return response.json()

    def get_notification_preferences(self):
        # Get notification preferences
        payload = {'monitor_id': '%s' % self.monitor_id}
        response = self.api_call('users/%s/notifications' %
                                 self.user_id, payload)
        return response.json()
    
    def get_trend_data(self, scale):
        if scale.upper() not in valid_scales:
            raise Exception("%s not a valid scale" % scale)
        t = datetime.now().replace(hour=12)
        response = self.api_call('app/history/trends?monitor_id=%s&scale=%s&start=%s' %
                                 (self.monitor_id, scale, t.isoformat()))
        self._trend_data_[scale] = response.json()

    def update_trend_data(self):
        for scale in valid_scales:
            self.get_trend_data(scale)

    def get_all_usage_data(self):
        payload = {'n_items': 30}
        # lots of info in here to be parsed out
        response = self.s.get('users/%s/timeline' %
                              self.user_id, payload)
        return response.json()



