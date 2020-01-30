import json
from flask import request
import subprocess
from subprocess import Popen
import codecs
import chardet
import re

def status_payload():
    b = subprocess.check_output(['mpc', 'status'])
    output = b.decode().split('\n')
    current_status = (re.search(r'\[([a-zA-Z]+)\]', output[1]).group(1) == "playing")
    song_artist = output[0].split(" - ")[0]
    song_title = output[0][len(song_artist)+3:]
    song_position = re.search(r'([0-9]+:[0-9]+)/', output[1]).group(1)
    song_total = re.search(r'/([0-9]+:[0-9]+)', output[1]).group(1)
    song_progress = re.search(r'([0-9:]+)%', output[1]).group(1)
    current_volume = re.search(r'volume: ([0-9]+)%', output[2]).group(1)
    current_sleep_timer_status = True
    try:
        subprocess.check_call("ps aux | grep sleep.sh | grep -v grep > /dev/null" , shell=True)
    except subprocess.CalledProcessError:
        current_sleep_timer_status = False
    payload = {
            'isplaying': current_status,
            'artist': song_artist,
            'title': song_title,
            'position': song_position,
            'total': song_total,
            'progress': song_progress,
            'volume': current_volume,
            'isSleepTimer': current_sleep_timer_status,
            }
    return payload

def handler_toggle():
    output = subprocess.check_output(['mpc', 'toggle'])
    status = re.search(r"\[[a-zA-Z]+\]", output.decode('utf-8'))
    payload = status_payload()
    return json.dumps(payload, ensure_ascii=False), 200

def handler_status():
    payload = status_payload()
    return json.dumps(payload, ensure_ascii=False), 200
        
def handler_next():
    output = subprocess.check_output(['mpc', 'next'])
    payload = status_payload()
    return json.dumps(payload, ensure_ascii=False), 200
        
def handler_prev():
    output = subprocess.check_output(['mpc', 'prev'])
    payload = status_payload()
    return json.dumps(payload, ensure_ascii=False), 200

def handler_sleep_timer():
    Popen("/home/pi/mochi/sleep.sh &", shell=True)
    payload = status_payload()
    return json.dumps(payload, ensure_ascii=False), 200

def handler_cancel_sleep_timer():
    Popen("pkill sleep", shell=True)
    payload = status_payload()
    return json.dumps(payload, ensure_ascii=False), 200

def handler_volume():
    volume = request.args.'num')
    if volume == None:
        output = subprocess.check_output(['mpc', 'volume'])
    else:
        output = subprocess.check_output(['mpc', 'volume', volume])

    status = re.search(r'volume:\s[0-9]+\%', output.decode('utf-8'))
    if status:
        return re.sub(r'[^0-9]','',status.group(0)), 200
    return 'failed', 500

def handler_request():
    param = request.args.get('param')
    if param == None:
        return 'require param', 400
    subprocess.check_output(['mpc', 'searchplay', param])
    payload = status_payload()
    return json.dumps(payload, ensure_ascii=False), 200

def handler_playlist_ls():
    cpi = subprocess.run(['mpc','lsplaylist'], stdout=subprocess.PIPE)
    ret = cpi.stdout.decode().split()
    return json.dumps(ret, ensure_ascii=False), 200

def handler_playlist_select():
    param = request.args.get('param')
    if param == None:
        return 'require param', 400
    subprocess.run(['mpc','clear'])
    cpi = subprocess.run(['mpc','load', param])
    if cpi.returncode != 0:
        return json.dumps(['error mpc load'], ensure_ascii=False), 200
    subprocess.run(['mpc','play'])
    payload = status_payload()
    return json.dumps(payload, ensure_ascii=False), 200

def handler_playlist_list():
    cpi = subprocess.run(['mpc', 'playlist', '-f', '%title%'], stdout=subprocess.PIPE)
    if cpi.returncode != 0:
        return json.dumps(['error mpc playlist'], ensure_ascii=False), 200
    ret = cpi.stdout.decode().split('\n')
    print(ret)
    return json.dumps(ret, ensure_ascii=False), 200

