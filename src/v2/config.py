import os
import sys

class Config:
    def __init__ (self):
        env = dict()
        _err_msg = []
        _env_list = [
            'MOCHI_APP_ROOT',
            'MOCHI_TAKO_RAW_ROOT',
            'MOCHI_TAKO_THUMBNAIL_ROOT',
            'MOCHI_OKONOMI_PATH',
            'MOCHI_NATUREREMO_TOKEN'
        ]

        for _env in _env_list:
            e = os.getenv(_env)
            if e == None:
                _err_msg.append('env ' + _env + ' must be set')
            env[_env] = e
            e = ''

        if len(_err_msg) != 0:
            print(_err_msg)
            sys.exit(1)

        self.ENV = env

    def get (self, key):
        if 'MOCHI_'+key in self.ENV:
            return self.ENV['MOCHI_'+key]
        print('err: Config: ' + 'MOCHI_' + key + ' not set')
        sys.exit(1)

if __name__ == '__main__':
    c = Config()
    print(c.get('APP_ROOT'))
