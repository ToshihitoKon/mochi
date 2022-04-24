from . import model
from flask import Blueprint, request
import json

class Hidamari:
    def __init__ (self, config):
        self.config = config
        self.model = model.get_model(config)

        router = Blueprint('hidamari', __name__, url_prefix='/api/v2/hidamari')

        @router.route('/light/on', methods=['POST'])
        def lightOn():
            ok, res = self.model.lightOn()
            if not ok:
                return json.dumps(res, ensure_ascii=False), 500
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/light/off', methods=['POST'])
        def lightOff():
            ok, res = self.model.lightOff()
            if not ok:
                return json.dumps(res, ensure_ascii=False), 500
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/light/preset_on', methods=['POST'])
        def lightPresetOn():
            ok, res = self.model.lightPresetOn()
            if not ok:
                return json.dumps(res, ensure_ascii=False), 500
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/light/preset_warm', methods=['POST'])
        def lightPresetWarm():
            ok, res = self.model.lightPresetWarm()
            if not ok:
                return json.dumps(res, ensure_ascii=False), 500
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/light/warm', methods=['POST'])
        def lightWarm():
            for num in range(3):
                ok, res = self.model.lightWarm()
                if not ok:
                    return json.dumps(res, ensure_ascii=False), 500
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/light/cool', methods=['POST'])
        def lightCool():
            for num in range(3):
                ok, res = self.model.lightCool()
                if not ok:
                    return json.dumps(res, ensure_ascii=False), 500
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/light/bright', methods=['POST'])
        def lightBright():
            for num in range(3):
                ok, res = self.model.lightBright()
                if not ok:
                    return json.dumps(res, ensure_ascii=False), 500
            return json.dumps(res, ensure_ascii=False), 200

        @router.route('/light/dim', methods=['POST'])
        def lightDim():
            for num in range(3):
                ok, res = self.model.lightDim()
                if not ok:
                    return json.dumps(res, ensure_ascii=False), 500
            return json.dumps(res, ensure_ascii=False), 200

        self.router = router

    def get_router(self): 
        return self.router
