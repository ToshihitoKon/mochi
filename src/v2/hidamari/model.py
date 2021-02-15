import flask
import os

def get_model(config):
    return Model(config)

class Model:
    def __init__(self, config):
        self._config = config
        self._natureremo_token = config.get('NATUREREMO_TOKEN')

    def lightToggle(self):

        return True
