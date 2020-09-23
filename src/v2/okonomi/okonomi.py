import os
import subprocess

okonomi_dir = os.path.expanduser('~/okonomi')
class Okonomi:
    def get_value(self, keys):
        res = subprocess.run([ okonomi_dir + '/kvs.sh', 'get'] + keys , stdout=subprocess.PIPE)

        kv = []
        rows = res.stdout.decode('utf-8').splitlines()
        for row in rows:
            key = row.split('\t')[0]
            value = row.split('\t')[1]
            kv.append({'key': key, 'value': value})
        return kv

    def get_group_value(self, group):
        res = subprocess.run([ okonomi_dir + '/kvs.sh', 'getgroup', group], stdout=subprocess.PIPE)

        kv = []
        rows = res.stdout.decode('utf-8').splitlines()
        for row in rows:
            key = row.split('\t')[0]
            value = row.split('\t')[1]
            kv.append({'key': key, 'value': value})
        return kv

    def set_value(self, key, value, group):
        res = subprocess.run([ okonomi_dir + '/kvs.sh', 'set', key, value, group] , stdout=subprocess.PIPE)
        return {'key': key, 'value': value}

    def set_group(self, key, group):
        res = subprocess.run([ okonomi_dir + '/kvs.sh', 'setgroup', key, group] , stdout=subprocess.PIPE)
        return {'key': key, 'group': group}

    def toggle_value(self, key):
        res = subprocess.run([ okonomi_dir + '/kvs.sh', 'toggle', key] , stdout=subprocess.PIPE)
        if not res.stdout:
            return {'key': key, 'value': ''}

        value = res.stdout.decode('utf-8').splitlines()[0].split('\t')[1]
        return {'key': key, 'value': value}

    def list_keys(self):
        res = subprocess.run([ okonomi_dir + '/kvs.sh', 'list'] , stdout=subprocess.PIPE)
        return res.stdout.decode('utf-8').splitlines()

    def list_groups(self):
        res = subprocess.run([ okonomi_dir + '/kvs.sh', 'listgroup'] , stdout=subprocess.PIPE)
        return res.stdout.decode('utf-8').splitlines()

if __name__ == '__main__':
    print(Okonomi().get_value(['key', 'key3']))
    print(Okonomi().list_groups())
    print(Okonomi().get_group_value('group'))
    print(Okonomi().set_value('key', 'false'))
    print(Okonomi().toggle_value('key'))
    print(Okonomi().list_keys())
