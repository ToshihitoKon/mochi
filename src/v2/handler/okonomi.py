from ..model import okonomi as model
from flask import Blueprint, request
import json

router = Blueprint('okonomi', __name__, url_prefix='/api/v2/okonomi')

@router.route('/get', methods=['GET'])
def get():
    key = request.args.get('key')
    if key:
        res = model.Okonomi().get_value([key])
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
    key = req['key']

    if 'value' not in req:
        return json.dumps('value must be required', ensure_ascii=False), 400
    value = req['value']

    group = ''
    if 'group' in req:
        group = req['group']

    res = model.Okonomi().set_value(key, value, group)
    return json.dumps(res, ensure_ascii=False), 200

@router.route('/toggle', methods=['POST'])
def toggle():
    req = request.get_json()
    if not req:
        return json.dumps(':thinking_face:', ensure_ascii=False), 400

    if 'key' not in req:
        return json.dumps('key must be required', ensure_ascii=False), 400
    key = req['key']

    res = model.Okonomi().toggle_value(req['key'])
    return json.dumps(res, ensure_ascii=False), 200

@router.route('/group/get', methods=['GET'])
def group_get():
    group = request.args.get('group')
    if not group:
        return json.dumps('', ensure_ascii=False), 400
    else:
        res = model.Okonomi().get_group_value(group)

    return json.dumps(res, ensure_ascii=False), 200

@router.route('/group/list', methods=['GET'])
def group_list():
    res = model.Okonomi().list_groups()
    return json.dumps(res, ensure_ascii=False), 200
