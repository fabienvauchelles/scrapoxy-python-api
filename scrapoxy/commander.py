"""
An SDK to wrap REST request over Scrapoxy API.
"""

# -*- coding: utf-8 -*-

import base64
import json
import requests


class Commander:

    def __init__(self, api, password):
        self._api = api
        self._password = base64.b64encode(password.encode())


    def get_instances(self):
        """Get all instances
        :return: All instances
        """

        headers = {
            'Authorization': self._password,
        }

        r = requests.get(u'{0}/instances'.format(self._api), headers=headers)

        if r.status_code == 200:
            return json.loads(r.content)

        else:
            r.raise_for_status()


    def stop_instance(self, name):
        """Stop an instance
        :param name: Instance name
        :return: The count of alive instances or -1 if the instance doesn't exist.
        """

        headers = {
            'Authorization': self._password,
        }

        payload = {
            'name': name
        }

        r = requests.post(u'{0}/instances/stop'.format(self._api), headers=headers, json=payload)

        if r.status_code == 404:
            return -1

        elif r.status_code == 200:
            result = json.loads(r.content)
            return result['alive']

        else:
            r.raise_for_status()


    def get_scaling(self):
        """Get the scaling
        :return: min, required, max
        """

        headers = {
            'Authorization': self._password,
        }

        r = requests.get(u'{0}/scaling'.format(self._api), headers=headers)

        if r.status_code == 200:
            result = json.loads(r.content)
            return result['min'], result['required'], result['max']

        else:
            r.raise_for_status()


    def update_scaling(self, min_sc, required_sc, max_sc):
        """Update the scaling
        :param min:
        :param required:
        :param max:
        :return: True if the scaling is updated or False if the scaling is the same.
        """

        headers = {
            'Authorization': self._password,
        }

        payload = {
            'min': min_sc,
            'required': required_sc,
            'max': max_sc,
        }

        r = requests.patch(u'{0}/scaling'.format(self._api), headers=headers, json=payload)

        if r.status_code == 204:
            return False

        elif r.status_code == 200:
            return True

        else:
            r.raise_for_status()


    def get_config(self):
        """Get the configuration
        :return: Configuration
        """

        headers = {
            'Authorization': self._password,
        }

        r = requests.get(u'{0}/config'.format(self._api), headers=headers)

        if r.status_code == 200:
            return json.loads(r.content)

        else:
            r.raise_for_status()


    def update_config(self, newconfig):
        """Update the configuration
        :param newconfig: The new configuration to merge (not replace)
        :return: True if the configuration is updated or False if the configuration is the same.
        """

        headers = {
            'Authorization': self._password,
        }

        r = requests.patch(u'{0}/config'.format(self._api), headers=headers, json=newconfig)

        if r.status_code == 204:
            return False

        elif r.status_code == 200:
            return True

        else:
            r.raise_for_status()
