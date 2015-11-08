# -*- coding: utf-8 -*-

import base64
import json
import requests


class Commander:

    def __init__(self, api, password):
        self._api = api
        self._password = base64.b64encode(password)


    def stop_instance(self, name):
        headers = {
            'Authorization': self._password,
        }

        payload = {
            'name': name
        }

        r = requests.post(u'{0}/instances/stop'.format(self._api), headers=headers, data=payload)

        if r.status_code == 404:
            return -1

        elif r.status_code == 200:
            result = json.loads(r.content)
            return result['alive']

        else:
            r.raise_for_status()
