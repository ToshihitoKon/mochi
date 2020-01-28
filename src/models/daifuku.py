import subprocess
import os
import json
from flask import request

root_path = '/home/pi'

def handler_mochi_pull():
    path = os.path.join(root_path, 'mochi', 'pull.sh')
    if not os.path.isfile(path):
        return 'error: ' + path + ' not found'

    cp = subprocess.run(path, capture_output=True, text=True)
    if cp.returncode != 0:
        res = {
            'status': 'error: ' + path + ' return not 0',
            'stdout': cp.stdout,
            'stderr': cp.stderr
        }
        return json.dumps(res, ensure_ascii=False)

    res = {
        'status': 'success',
        'stdout': cp.stdout,
        'stderr': cp.stderr
    }
    return json.dumps(res, ensure_ascii=False)

def handler_kashiwa_pull():
    path = os.path.join(root_path, 'kashiwa', 'pull.sh')
    if not os.path.isfile(path):
        return 'error: ' + path + ' not found'

    cp = subprocess.run(path, capture_output=True, text=True)
    if cp.returncode != 0:
        res = {
            'status': 'error: ' + path + ' return not 0',
            'stdout': cp.stdout,
            'stderr': cp.stderr
        }
        return json.dumps(res, ensure_ascii=False)

    res = {
        'status': 'success',
        'stdout': cp.stdout,
        'stderr': cp.stderr
    }
    return json.dumps(res, ensure_ascii=False)
