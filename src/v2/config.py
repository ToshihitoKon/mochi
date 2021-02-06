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
        ]

        for _env in _env_list:
            env[_env] = os.getenv(_env)
            if env[_env] == None:
                _err_msg.append('env ' + _env + ' must be set')

        if len(_err_msg) != 0:
            print(_err_msg)
            sys.exit(1)

        self.ENV = env

    def get (self, key):
        if key in self.ENV:
            return self.ENV[key]
        return None

    def must(self, key):
        if key in self.ENV:
            return self.ENV[key]
        print('err: Config: ' + key + ' not set')
        sys.exit(1)


if __name__ == '__main__':
    c = Config()
    print(c.get('MOCHI_APP_ROOT'))
    print(c.get('aaa'))
    print(c.must('MOCHI_APP_ROOT'))
    print(c.must('aaa'))
