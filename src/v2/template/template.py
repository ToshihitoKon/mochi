import flask
import os

def get_model(config):
    return Model(config)

class Template:
    def __init__(self, config):
        self._config = config

    def func(self, arg):
        return True
