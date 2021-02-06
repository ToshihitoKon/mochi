from . import tako
from flask import Blueprint, request
import json

class Tako:
    def __init__ (self, config):
        self.config = config
        self.model = tako.get_model(config)

        router = Blueprint('tako', __name__, url_prefix='/api/v2/tako')

        @router.route('/data/upload', methods=['POST'])
        def upload_multipart():
            if 'uploadFile' not in request.files:
                return json.dumps('', ensure_ascii=False), 400

            recievedFile = request.files['uploadFile']
            if self.model.save_file(recievedFile):
                return json.dumps('ok', ensure_ascii=False), 200
            else:
                return json.dumps('failed', ensure_ascii=False), 500

        @router.route('/list', methods=['GET'])
        def list():
            filelist = self.model.list_file()
            return json.dumps(filelist, ensure_ascii=False), 200

        @router.route('/data/get/<string:path>', methods=['GET'])
        def get_file(path):
            target = self.model.serve_file(path)
            if not target:
                return json.dumps('', ensure_ascii=False), 404
            return target

        self.router = router

    def get_router(self): 
        return self.router
