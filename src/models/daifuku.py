import subprocess
import os

root_path = '/home/pi'

def handler_mochi_pull():
    path = os.path.join(root_path, 'mochi', 'pull.sh')
    if not os.path.isfile(path):
        return 'error: ' + path + ' not found'

    cp = subprocess.run(path)
    if cp.returncode != 0:
        return 'error: ' + path + ' return not 0'

    return 'success'

def handler_kashiwa_pull():
    path = os.path.join(root_path, 'kashiwa', 'pull.sh')
    if not os.path.isfile(path):
        return 'error: ' + path + ' not found'

    cp = subprocess.run(path)
    if cp.returncode != 0:
        return 'error: ' + path + ' return not 0'

    return 'success'