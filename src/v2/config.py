import os
import sys

class Config:
    _prefix='MOCHI_'

    def __init__ (self):
        env = dict()
        _err_msg = []
        _env_list = [
            'APP_ROOT',
            'TAKO_RAW_ROOT',
            'TAKO_THUMBNAIL_ROOT',
            'OKONOMI_PATH',
            'NATUREREMO_TOKEN',
            'NATUREREMO_LIGHT_SIGSWITCH',
            'NATUREREMO_LIGHT_SIGWARM',
            'NATUREREMO_LIGHT_SIGCOOL',
        ]

        for _env in _env_list:
            e = os.getenv(self._prefix + _env)
            if e == None:
                _err_msg.append('env ' + _prefix + _env + ' must be set')
            env[self._prefix+_env] = e
            e = ''

        if len(_err_msg) != 0:
            for msg in _err_msg:
                print(msg)
            sys.exit(1)

        self.ENV = env

    def get (self, key):
        if self._prefix+key in self.ENV:
            return self.ENV[self._prefix+key]
        print('err: Config: ' + self._prefix + key + ' not set')
        sys.exit(1)

if __name__ == '__main__':
    c = Config()
    print(c.get('APP_ROOT'))
