from . import mpd
from flask import Blueprint, request
import json


class Music:
    def get_router(self): 
        return self.router

    def __init__ (self, config):
        self.config = config
        self.model = mpd.get_model(config)

        router = Blueprint('music', __name__, url_prefix='/api/v2')

        @router.route('/toggle', methods=['POST'])
        def toggle():
            res = self.model.toggle_play()
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/next', methods=['POST'])
        def next():
            res = self.model.next()
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/prev', methods=['POST'])
        def prev():
            res = self.model.prev()
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/play/position', methods=['POST'])
        def play_position():
            req = request.get_json()
            if not req:
                return json.dumps('', ensure_ascii=False), 400

            if 'position' not in req:
                return json.dumps('', ensure_ascii=False), 400

            res = self.model.play_position(req["position"])
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/status', methods=['GET'])
        def status():
            res = self.model.get_status()
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/playlist/current', methods=['GET'])
        def playlist_current():
            res = self.model.get_playlist()
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/playlist/list', methods=['GET'])
        def playlist_list():
            res = self.model.get_playlist_list()
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/playlist/select', methods=['POST'])
        def playlist_select():
            req = request.get_json()
            if not req:
                return json.dumps('', ensure_ascii=False), 400

            if 'name' not in req:
                return json.dumps('', ensure_ascii=False), 400

            if not self.model.playlist_select(req["name"]):
                return json.dumps("", ensure_ascii=False), 500
            res = self.model.get_playlist()
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/crop', methods=['POST'])
        def crop():
            if not self.model.crop():
                return json.dumps("", ensure_ascii=False), 500
            res = self.model.get_playlist()
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/queue/add', methods=['POST'])
        def queue_add():
            req = request.get_json()
            if not req:
                return json.dumps('', ensure_ascii=False), 400
            if 'path' not in req:
                return json.dumps('', ensure_ascii=False), 400

            if not self.model.queue_add(req["path"]):
                return json.dumps("", ensure_ascii=False), 500
            res = self.model.get_playlist()
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/volume', methods=['POST'])
        def volume():
            req = request.get_json()
            if not req:
                return json.dumps('', ensure_ascii=False), 400

            if 'volume' not in req:
                return json.dumps('', ensure_ascii=False), 400

            res = self.model.volume(req["volume"])
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/mode', methods=['POST'])
        def mode():
            req = request.get_json()
            if not req:
                return json.dumps('', ensure_ascii=False), 400
            if 'mode' not in req:
                return json.dumps('mode must be required', ensure_ascii=False), 400
            if 'state' not in req:
                return json.dumps('state must be required', ensure_ascii=False), 400

            res = self.model.set_player_mode(req["mode"], req["state"])
            if not res:
                return json.dumps(res, ensure_ascii=False), 500
            return json.dumps(res, ensure_ascii=False), 200

        # TODO: 雑実装
        @router.route('/sleeptimer/reset', methods=['POST'])
        def sleeptimer_reset():
            res =  self.model.reset_sleeptimer()
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/sleeptimer/cancel', methods=['POST'])
        def sleeptimer_cancel():
            res = self.model.cancel_sleeptimer()
            return json.dumps(res, ensure_ascii=False), 200


        @router.route('/search/fetchall', methods=['GET'])
        def file_fetchall():
            res = self.model.fetch_musicdir()
            if not res:
                return json.dumps(res, ensure_ascii=False), 500
            return json.dumps(res, ensure_ascii=False), 200

        self.router = router
