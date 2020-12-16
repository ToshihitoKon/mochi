import subprocess
from flask import Blueprint, request
import json

router = Blueprint('script_kicker', __name__, url_prefix='/api/v2/script_kicker')

@router.route('/kick', methods=['POST'])
def kick():
    req = request.get_json()
    if not req:
        return json.dumps(':thinking_face:', ensure_ascii=False), 400
    if 'target' not in req:
        return json.dumps('key must be required', ensure_ascii=False), 400
    target = req['target']

    res = subprocess.run(['bash', '-c', '~/natureremo/' + target + '.sh'] , stdout=subprocess.PIPE)
    return json.dumps(res.returncode, ensure_ascii=False), 200

