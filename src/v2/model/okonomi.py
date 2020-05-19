import os
import subprocess

okonomi_dir = os.path.expanduser('~/mochi/okonomi')
class Okonomi:
    def get_value(self, key):
        res = subprocess.run([ okonomi_dir + '/kvs.sh', 'get', key] , stdout=subprocess.PIPE)
        if not res.stdout:
            return {'key': key, 'value': ''}

        value = res.stdout.decode('utf-8').splitlines()[1]
        return {'key': key, 'value': value}

    def set_value(self, key, value):
        res = subprocess.run([ okonomi_dir + '/kvs.sh', 'set', key, value] , stdout=subprocess.PIPE)
        return {'key': key, 'value': value}

    def toggle_value(self, key):
        res = subprocess.run([ okonomi_dir + '/kvs.sh', 'toggle', key] , stdout=subprocess.PIPE)
        if not res.stdout:
            return {'key': key, 'value': ''}

        value = res.stdout.decode('utf-8').splitlines()[1]
        return {'key': key, 'value': value}

    def list_keys(self):
        res = subprocess.run([ okonomi_dir + '/kvs.sh', 'list'] , stdout=subprocess.PIPE)
        return res.stdout.decode('utf-8').splitlines()

if __name__ == '__main__':
    print(Okonomi().get_value('key'))
    print(Okonomi().set_value('key', 'false'))
    print(Okonomi().toggle_value('key'))
    print(Okonomi().list_keys())
