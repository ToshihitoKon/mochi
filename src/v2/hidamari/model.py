import flask
import os
import urllib.request
import urllib.response

def get_model(config):
    return Model(config)

class Model:
    def __init__(self, config):
        self._config = config
        self._natureremo = {
            'token': config.get('NATUREREMO_TOKEN'),
            'light': {
                'switch': config.get('NATUREREMO_LIGHT_SIGSWITCH'),
                'warm': config.get('NATUREREMO_LIGHT_SIGWARM'),
                'cool': config.get('NATUREREMO_LIGHT_SIGCOOL'),
                'bright': config.get('NATUREREMO_LIGHT_SIGBRIGHT'),
                'dim': config.get('NATUREREMO_LIGHT_SIGDIM'),
            }
        } 

    def lightSwitch(self):
        url = 'https://api.nature.global/1/signals/'+self._natureremo['light']['switch']+'/send'
        return self.natureremoSend(url)

    def lightWarm(self):
        url = 'https://api.nature.global/1/signals/'+self._natureremo['light']['warm']+'/send'
        return self.natureremoSend(url)

    def lightCool(self):
        url = 'https://api.nature.global/1/signals/'+self._natureremo['light']['cool']+'/send'
        return self.natureremoSend(url)

    def lightBright(self):
        url = 'https://api.nature.global/1/signals/'+self._natureremo['light']['bright']+'/send'
        return self.natureremoSend(url)

    def lightDim(self):
        url = 'https://api.nature.global/1/signals/'+self._natureremo['light']['dim']+'/send'
        return self.natureremoSend(url)

    def lightSwitch(self):
        url = 'https://api.nature.global/1/signals/'+self._natureremo['light']['switch']+'/send'
        return self.natureremoSend(url)

    def natureremoSend(self, url):
        data = {}
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer '+self._natureremo['token'],
        }
        req = urllib.request.Request(url, data, headers)
        try:
            res = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            return False, {
                    'status': e.code,
                    'rate_remaining':e.headers.get('X-Rate-Limit-Remaining', ''),
                    'rate_reset': e.headers.get('X-Rate-Limit-Reset', ''),
                }
        except Exception as e:
            return False, {
                    'status': 'error unexpected',
                    'rate_remaining':'',
                    'rate_reset': '',
                }
        return True, {
                'status': res.code,
                'rate_remaining':res.headers.get('X-Rate-Limit-Remaining', ''),
                'rate_reset': res.headers.get('X-Rate-Limit-Reset', ''),
            }


