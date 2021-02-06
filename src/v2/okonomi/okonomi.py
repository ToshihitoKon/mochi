import os
import subprocess

def get_model(config):
    return Model(config)

class Model:
    def __init__(self, config):
        self.config = config
        self.okonomi_path = config.must('MOCHI_OKONOMI_PATH')

    def get_value(self, keys):
        res = subprocess.run([ self.okonomi_path, 'get'] + keys , stdout=subprocess.PIPE)

        kv = []
        rows = res.stdout.decode('utf-8').splitlines()
        for row in rows:
            key = row.split('\t')[0]
            value = row.split('\t')[1]
            kv.append({'key': key, 'value': value})
        return kv

    def get_group_value(self, group):
        res = subprocess.run([ self.okonomi_path, 'getgroup', group], stdout=subprocess.PIPE)

        kv = []
        rows = res.stdout.decode('utf-8').splitlines()
        for row in rows:
            key = row.split('\t')[0]
            value = row.split('\t')[1]
            kv.append({'key': key, 'value': value})
        return kv

    def set_value(self, key, value, group):
        res = subprocess.run([ self.okonomi_path, 'set', key, value, group] , stdout=subprocess.PIPE)
        return {'key': key, 'value': value}

    def set_group(self, key, group):
        res = subprocess.run([ self.okonomi_path, 'setgroup', key, group] , stdout=subprocess.PIPE)
        return {'key': key, 'group': group}

    def toggle_value(self, key):
        res = subprocess.run([ self.okonomi_path, 'toggle', key] , stdout=subprocess.PIPE)
        if not res.stdout:
            return {'key': key, 'value': ''}

        value = res.stdout.decode('utf-8').splitlines()[0].split('\t')[1]
        return {'key': key, 'value': value}

    def list_keys(self):
        res = subprocess.run([ self.okonomi_path, 'list'] , stdout=subprocess.PIPE)
        return res.stdout.decode('utf-8').splitlines()

    def list_groups(self):
        res = subprocess.run([ self.okonomi_path, 'listgroup'] , stdout=subprocess.PIPE)
        return res.stdout.decode('utf-8').splitlines()
