#!/usr/bin/env python3
from flask import Flask, request
from flask_cors import CORS
from models.mpd import *
from models.daifuku import *

class FlaskWrap:
    def __init__(self):
        self.flask = Flask(__name__)
        CORS(self.flask)

    def set_handler(self, path, handle_func):
        self.flask.add_url_rule(path, view_func=handle_func) 
    
    def debug_run(self):
        self.flask.run(port=8880, debug=True)
    
class FlaskHandler:
    def __init__(self, path, handler_func):
        self.path = path
        self.handler_func = handler_func

    def to_set_handler(self):
        return self.path, self.handler_func

def echo_handler(var='ok'):
    return var, 200

flask_handlers = []

flask_handlers.append(FlaskHandler('/echo', echo_handler))

flask_handlers.append(FlaskHandler('/api/toggle', handler_toggle))
flask_handlers.append(FlaskHandler('/api/status', handler_status))
flask_handlers.append(FlaskHandler('/api/next', handler_next))
flask_handlers.append(FlaskHandler('/api/prev', handler_prev))
flask_handlers.append(FlaskHandler('/api/sleepTimer', handler_sleep_timer))
flask_handlers.append(FlaskHandler('/api/cancelSleepTimer', handler_cancel_sleep_timer))
flask_handlers.append(FlaskHandler('/api/volume', handler_volume))
flask_handlers.append(FlaskHandler('/api/request', handler_request))
flask_handlers.append(FlaskHandler('/api/playlist/ls', handler_playlist_ls))
flask_handlers.append(FlaskHandler('/api/playlist/select', handler_playlist_select))
flask_handlers.append(FlaskHandler('/api/playlist/list', handler_playlist_list))

flask_handlers.append(FlaskHandler('/daifuku/mochi/pull', handler_mochi_pull))
flask_handlers.append(FlaskHandler('/daifuku/kashiwa/pull', handler_kashiwa_pull))
