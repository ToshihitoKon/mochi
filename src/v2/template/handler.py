from . import tako
from flask import Blueprint, request
import json

class Template:
    def __init__ (self, config):
        self.config = config
        #self.model = template.get_model(config)

        router = Blueprint('template', __name__, url_prefix='/api/v2/template')

        @router.route('/handle/path', methods=['POST'])
        def handlerFunc():
            result = self.model.func()
            return json.dumps(result, ensure_ascii=False), 200

        self.router = router

    def get_router(self): 
        return self.router
