from . import tako as model
from flask import Blueprint, request
import json

router = Blueprint('tako', __name__, url_prefix='/api/v2/tako')

@router.route('/data/upload', methods=['POST'])
def upload_multipart():
    if 'uploadFile' not in request.files:
        return json.dumps('', ensure_ascii=False), 400

    recievedFile = request.files['uploadFile']
    if model.Tako().save_file(recievedFile):
        return json.dumps('ok', ensure_ascii=False), 200
    else:
        return json.dumps('failed', ensure_ascii=False), 500

@router.route('/list', methods=['GET'])
def list():
    filelist = model.Tako().list_file()
    return json.dumps(filelist, ensure_ascii=False), 200

@router.route('/data/get/<string:path>', methods=['GET'])
def get_file(path):
    target = model.Tako().serve_file(path)
    if not target:
        return json.dumps('', ensure_ascii=False), 404
    return target
