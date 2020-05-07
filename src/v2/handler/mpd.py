from ..model import mpd as mpdmodel
from flask import Blueprint, request
import json

mpd_router = Blueprint('mpd', __name__, url_prefix='/api/v2')

@mpd_router.route('/toggle', methods=['POST'])
def toggle():
    res = mpdmodel.Mpd().toggle_play()
    return json.dumps(res, ensure_ascii=False), 200

@mpd_router.route('/next', methods=['POST'])
def next():
    res = mpdmodel.Mpd().next()
    return json.dumps(res, ensure_ascii=False), 200

@mpd_router.route('/prev', methods=['POST'])
def prev():
    res = mpdmodel.Mpd().prev()
    return json.dumps(res, ensure_ascii=False), 200

@mpd_router.route('/status', methods=['GET'])
def status():
    res = mpdmodel.Mpd().get_status()
    return json.dumps(res, ensure_ascii=False), 200

@mpd_router.route('/playlist/current', methods=['GET'])
def playlist_current():
    res = mpdmodel.Mpd().get_playlist()
    return json.dumps(res, ensure_ascii=False), 200

@mpd_router.route('/playlist/list', methods=['GET'])
def playlist_list():
    res = mpdmodel.Mpd().get_playlist_list()
    return json.dumps(res, ensure_ascii=False), 200

@mpd_router.route('/volume', methods=['POST'])
def volume():
    req = request.get_json()
    if not req:
        return json.dumps('', ensure_ascii=False), 400

    if 'volume' not in req:
        return json.dumps('', ensure_ascii=False), 400

    res = mpdmodel.Mpd().volume(req["volume"])
    return json.dumps(res, ensure_ascii=False), 200
