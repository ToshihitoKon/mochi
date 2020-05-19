#!/usr/bin/env python3
from v1.models import mpd as mpdv1
from v1.models import daifuku as daifukuv1
from v2.handler import mpd as mpdv2
from v2.handler import okonomi as okonomi


# v2
blueprints = [
    mpdv2.mpd_router,
    okonomi.router
]

###
# v1時代の遺産
class FlaskHandler:
    def __init__(self, path, handler_func, methods=['GET','POST']):
        self.path = path
        self.handler_func = handler_func
        self.methods = methods

    def to_set_handler(self):
        return self.path, self.handler_func, self.methods

def echo_handler(var='ok'):
    return var, 200

flask_handlers = []

flask_handlers.append(FlaskHandler('/echo', echo_handler))

# v1
# mpd api
flask_handlers.append(FlaskHandler('/api/toggle', mpdv1.handler_toggle))
flask_handlers.append(FlaskHandler('/api/status', mpdv1.handler_status))
flask_handlers.append(FlaskHandler('/api/next', mpdv1.handler_next))
flask_handlers.append(FlaskHandler('/api/prev', mpdv1.handler_prev))
flask_handlers.append(FlaskHandler('/api/sleepTimer', mpdv1.handler_sleep_timer))
flask_handlers.append(FlaskHandler('/api/cancelSleepTimer', mpdv1.handler_cancel_sleep_timer))
flask_handlers.append(FlaskHandler('/api/volume', mpdv1.handler_volume))
flask_handlers.append(FlaskHandler('/api/request', mpdv1.handler_request))
flask_handlers.append(FlaskHandler('/api/playlist/ls', mpdv1.handler_playlist_ls))
flask_handlers.append(FlaskHandler('/api/playlist/select', mpdv1.handler_playlist_select))
flask_handlers.append(FlaskHandler('/api/playlist/list', mpdv1.handler_playlist_list))

# daifuku api
flask_handlers.append(FlaskHandler('/daifuku/mochi/pull', daifukuv1.handler_mochi_pull, ['POST']))
flask_handlers.append(FlaskHandler('/daifuku/mochi/version', daifukuv1.handler_mochi_version, ['POST']))
flask_handlers.append(FlaskHandler('/daifuku/kashiwa/pull', daifukuv1.handler_kashiwa_pull, ['POST']))
flask_handlers.append(FlaskHandler('/daifuku/kashiwa/version', daifukuv1.handler_kashiwa_version, ['POST']))
