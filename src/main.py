#!/usr/bin/env python3
from handler import *

class FlaskWrap:
    def __init__(self):
        self.flask = Flask(__name__)
        CORS(self.flask)

    def set_handler(self, path, handle_func):
        self.flask.add_url_rule(path, view_func=handle_func, methods=['GET', 'POST']) 
    
    def debug_run(self):
        self.flask.run(port=8880, debug=True)
    
flask = FlaskWrap()
app = flask.flask

for flask_handler in flask_handlers:
    path, handler = flask_handler.to_set_handler()
    flask.set_handler(path, handler)

if __name__ == '__main__':
    flask.debug_run()
