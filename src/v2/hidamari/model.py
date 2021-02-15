import flask
import os

def get_model(config):
    return Model(config)

class Model:
    def __init__(self, config):
        self._config = config

    def lightToggle(self):
        return True
