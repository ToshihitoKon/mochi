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
