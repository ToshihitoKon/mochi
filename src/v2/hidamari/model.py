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
            'appliance': config.get('NATUREREMO_LIGHT_APPLIANCE'),
            'button': {
                'on': config.get('NATUREREMO_LIGHT_BUTTON_ON'),
                'off': config.get('NATUREREMO_LIGHT_BUTTON_OFF'),
                'bright': config.get('NATUREREMO_LIGHT_BUTTON_BLIGHT'),
                'dim': config.get('NATUREREMO_LIGHT_BUTTON_DIM'),
                'warm': config.get('NATUREREMO_LIGHT_BUTTON_WARM'),
                'cool': config.get('NATUREREMO_LIGHT_BUTTON_COOL'),
                'preset_on': config.get('NATUREREMO_LIGHT_BUTTON_PRESET_ON'),
            },
            'signal': {
                'preset_warm':config.get('NATUREREMO_LIGHT_SIGNAL_PRESET_WARM'),   
            }
        } 

    def lightOn(self):
        return self.natureremoSendButton(self._natureremo['button']['on'])

    def lightOff(self):
        return self.natureremoSendButton(self._natureremo['button']['off'])

    def lightPresetWarm(self):
        return self.natureremoSendSignal(self._natureremo['signal']['preset_warm'])

    def lightPresetOn(self):
        return self.natureremoSendButton(self._natureremo['button']['preset_on'])

    def lightWarm(self):
        return self.natureremoSendButton(self._natureremo['button']['warm'])

    def lightCool(self):
        return self.natureremoSendButton(self._natureremo['button']['cool'])

    def lightBright(self):
        return self.natureremoSendButton(self._natureremo['button']['bright'])

    def lightDim(self):
        return self.natureremoSendButton(self._natureremo['button']['dim'])

    def natureremoSendButton(self, button):
        url = f"https://api.nature.global/1/appliances/{self._natureremo['appliance']}/light"
        data = urllib.parse.urlencode({
                'button': button,
            })
        print(data)
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer '+self._natureremo['token'],
        }
        return self._send(url, data.encode('utf-8'), headers)

    def natureremoSendSignal(self, signal):
        url = f"https://api.nature.global/1/signals/{signal}/send"
        data = {}
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer '+self._natureremo['token'],
        }
        return self._send(url, data, headers)

    def _send(self, url, data, headers):
        req = urllib.request.Request(url, data, headers)
        try:
            res = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print(e)
            return False, {
                    'status': e.code,
                    'rate_remaining':e.headers.get('X-Rate-Limit-Remaining', ''),
                    'rate_reset': e.headers.get('X-Rate-Limit-Reset', ''),
                }
        except Exception as e:
            print(e)
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


