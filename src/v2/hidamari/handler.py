from . import model
from flask import Blueprint, request
import json

class Hidamari:
    def __init__ (self, config):
        self.config = config
        self.model = model.get_model(config)

        router = Blueprint('hidamari', __name__, url_prefix='/api/v2/hidamari')

        @router.route('/light/toggle', methods=['POST'])
        def lightToggle():
            result = self.model.lightToggle()
            return json.dumps(result, ensure_ascii=False), 200

        self.router = router

    def get_router(self): 
        return self.router
