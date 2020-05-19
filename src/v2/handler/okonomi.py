from ..model import okonomi as model
from flask import Blueprint, request
import json

router = Blueprint('okonomi', __name__, url_prefix='/api/v2/okonomi')

@router.route('/get', methods=['GET'])
def get():
    key = request.args.get('key')
    if key:
        res = model.Okonomi().get_value(key)
    else:
        res = model.Okonomi().list_keys()

    return json.dumps(res, ensure_ascii=False), 200

@router.route('/set', methods=['POST'])
def set():
    req = request.get_json()
    if not req:
        return json.dumps(':thinking_face:', ensure_ascii=False), 400

    if 'key' not in req:
        return json.dumps('key must be required', ensure_ascii=False), 400

    if 'value' not in req:
        return json.dumps('value must be required', ensure_ascii=False), 400

    res = model.Okonomi().set_value(key, value)
    return json.dumps(res, ensure_ascii=False), 200

@router.route('/toggle', methods=['POST'])
def toggle():
    req = request.get_json()
    if not req:
        return json.dumps(':thinking_face:', ensure_ascii=False), 400

    if 'key' not in req:
        return json.dumps('key must be required', ensure_ascii=False), 400

    res = model.Okonomi().toggle_value(key)
    return json.dumps(res, ensure_ascii=False), 200
