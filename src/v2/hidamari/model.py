import flask
import os
import urllib.request

def get_model(config):
    return Model(config)

class Model:
    def __init__(self, config):
        self._config = config
        self._natureremo_token = config.get('NATUREREMO_TOKEN')

    def lightToggle(self):
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer '+self._natureremo_token,
        }

        return True
