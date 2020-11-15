from . import mpd as mpdmodel
from flask import Blueprint, request
import json

music_router = Blueprint('music', __name__, url_prefix='/api/v2')

@music_router.route('/toggle', methods=['POST'])
def toggle():
    res = mpdmodel.Mpd().toggle_play()
    return json.dumps(res, ensure_ascii=False), 200

@music_router.route('/next', methods=['POST'])
def next():
    res = mpdmodel.Mpd().next()
    return json.dumps(res, ensure_ascii=False), 200

@music_router.route('/prev', methods=['POST'])
def prev():
    res = mpdmodel.Mpd().prev()
    return json.dumps(res, ensure_ascii=False), 200

@music_router.route('/play/position', methods=['POST'])
def play_position():
    req = request.get_json()
    if not req:
        return json.dumps('', ensure_ascii=False), 400

    if 'position' not in req:
        return json.dumps('', ensure_ascii=False), 400

    res = mpdmodel.Mpd().play_position(req["position"])
    return json.dumps(res, ensure_ascii=False), 200

@music_router.route('/status', methods=['GET'])
def status():
    res = mpdmodel.Mpd().get_status()
    return json.dumps(res, ensure_ascii=False), 200

@music_router.route('/playlist/current', methods=['GET'])
def playlist_current():
    res = mpdmodel.Mpd().get_playlist()
    return json.dumps(res, ensure_ascii=False), 200

@music_router.route('/playlist/list', methods=['GET'])
def playlist_list():
    res = mpdmodel.Mpd().get_playlist_list()
    return json.dumps(res, ensure_ascii=False), 200

@music_router.route('/playlist/select', methods=['POST'])
def playlist_select():
    req = request.get_json()
    if not req:
        return json.dumps('', ensure_ascii=False), 400

    if 'name' not in req:
        return json.dumps('', ensure_ascii=False), 400

    if not mpdmodel.Mpd().playlist_select(req["name"]):
        return json.dumps("", ensure_ascii=False), 500
    res = mpdmodel.Mpd().get_playlist()
    return json.dumps(res, ensure_ascii=False), 200

@music_router.route('/crop', methods=['POST'])
def crop():
    if not mpdmodel.Mpd().crop():
        return json.dumps("", ensure_ascii=False), 500
    res = mpdmodel.Mpd().get_playlist()
    return json.dumps(res, ensure_ascii=False), 200

@music_router.route('/queue/add', methods=['POST'])
def queue_add():
    req = request.get_json()
    if not req:
        return json.dumps('', ensure_ascii=False), 400
    if 'path' not in req:
        return json.dumps('', ensure_ascii=False), 400

    if not mpdmodel.Mpd().queue_add(req["path"]):
        return json.dumps("", ensure_ascii=False), 500
    res = mpdmodel.Mpd().get_playlist()

@music_router.route('/volume', methods=['POST'])
def volume():
    req = request.get_json()
    if not req:
        return json.dumps('', ensure_ascii=False), 400

    if 'volume' not in req:
        return json.dumps('', ensure_ascii=False), 400

    res = mpdmodel.Mpd().volume(req["volume"])
    return json.dumps(res, ensure_ascii=False), 200

@music_router.route('/mode', methods=['POST'])
def mode():
    req = request.get_json()
    if not req:
        return json.dumps('', ensure_ascii=False), 400
    if 'mode' not in req:
        return json.dumps('mode must be required', ensure_ascii=False), 400
    if 'state' not in req:
        return json.dumps('state must be required', ensure_ascii=False), 400

    res = mpdmodel.Mpd().set_player_mode(req["mode"], req["state"])
    if not res:
        return json.dumps(res, ensure_ascii=False), 500
    return json.dumps(res, ensure_ascii=False), 200

# TODO: 雑実装
@music_router.route('/sleeptimer/reset', methods=['POST'])
def sleeptimer_reset():
    res =  mpdmodel.Mpd().reset_sleeptimer()
    return json.dumps(res, ensure_ascii=False), 200

@music_router.route('/sleeptimer/cancel', methods=['POST'])
def sleeptimer_cancel():
    res = mpdmodel.Mpd().cancel_sleeptimer()
    return json.dumps(res, ensure_ascii=False), 200


@music_router.route('/search/fetchall', methods=['GET'])
def file_fetchall():
    res = mpdmodel.Mpd().fetch_musicdir()
    if not res:
        return json.dumps(res, ensure_ascii=False), 500
    return json.dumps(res, ensure_ascii=False), 200
