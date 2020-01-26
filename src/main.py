#!/usr/bin/env python3
from handler import *

flask = FlaskWrap()
app = flask.flask

for flask_handler in flask_handlers:
    path, handler = flask_handler.to_set_handler()
    flask.set_handler(path, handler)

if __name__ == '__main__':
    flask.debug_run()
