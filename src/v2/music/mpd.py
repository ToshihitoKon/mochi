import subprocess
import regex
import pathlib
import os

format_option = ['-f', '%position%\t%title%\t%artist%\t%album%\t%file%']

def get_model(config):
    return Model(config)

# listallのパース
def nestedupdate(srcdict, destdict):
    for k, v in srcdict.items():
        if k in destdict:
            if isinstance(destdict[k], dict):
                return nestedupdate(v, destdict[k])
            elif isinstance(destdict[k], list) and isinstance(v, list):
                destdict[k].extend(v)
            else:
                destdict[k] = v
        else:
            destdict[k] = v
    return destdict

class Model:
    _is_playing = False
    _title = ''
    _artist = ''
    _playlist_pos = -1
    _album = ''
    _filepath = ''
    _volume = -1
    _duration = -1
    _total = -1
    _progress = -1
    _repeat = False
    _random = False
    _single = False
    _consume = False
    _sleeptimer = False

    def __init__(self, config):
        self.config = config
        self.mochi_dir = config.must('MOCHI_APP_ROOT')
    
    def parse_mpc_output(self, output):
        if output.find('ERROR') != -1:
            print("error: ", output)
            return False

        res = subprocess.run("ps aux | grep sleep.sh | grep -v grep" , shell=True, stdout=subprocess.PIPE)
        if not res.stdout.decode('utf-8'):
            self._sleeptimer = False
        else:
            self._sleeptimer = True


        try:
            rows = output.splitlines()
            if len(rows) == 1:
                # song not set
                self._title = ''
                self._artist = ''
                self._is_playing = False
                status_line = rows[0]
            elif len(rows) == 3:
                # song set
                song_line = rows[0].split('\t')
                self._playlist_pos = song_line[0]
                self._title = song_line[1]
                self._artist = song_line[2]
                self._album = song_line[3]
                self._filepath =  song_line[4]

                player_line = rows[1]
                self._is_playing = (player_line.find('playing') != -1)
                song_length =  regex.search(r'(?P<dur>\d+:\d+)/(?P<tot>\d+:\d+).*\((?P<pro>\d+)%\)', player_line)
                self._progress = song_length.group('pro')

                split_duration = song_length.group('dur').split(':')
                self._duration = int(split_duration[0])*60 + int(split_duration[1])
                split_total = song_length.group('tot').split(':')
                self._total = int(split_total[0])*60 + int(split_total[1])


                status_line = rows[2]
            else:
                return False

            status_match = regex.search(
                    r'volume:\s*(?<vol>[^\s]+)\s+'
                    'repeat:\s+(?<rep>[^\s]+)\s+'
                    'random:\s+(?<ran>[^\s]+)\s+'
                    'single:\s+(?<sin>[^\s]+)\s+'
                    'consume:\s+(?<con>[^\s]+).*', status_line)

            volume = status_match.group('vol').replace('%', '')
            if volume.isdecimal():
                self._volume = int(volume)
            else:
                self._volume = -1

            self._repeat = status_match.group('rep') == "on"
            self._random = status_match.group('ran') == "on"
            self._single = status_match.group('sin') == "on"
            self._consume = status_match.group('con') == "on"
            return True
        except:
            return False

    def status_object(self):
        return {
                'isplaying': self._is_playing,
                'artist': self._artist,
                'title': self._title,
                'playlist_position': self._playlist_pos,
                'album': self._album,
                'filepath': self._filepath,
                'duration': self._duration,
                'total': self._total,
                'progress': self._progress,
                'volume': self._volume,
                'repeat': self._repeat,
                'random': self._random,
                'single': self._single,
                'consume': self._consume,
                'sleeptimer': self._sleeptimer
        }

    def get_status(self):
        res = subprocess.run(['mpc'] + format_option + ['status'] , stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()


    def get_playlist(self):
        res = subprocess.run(['mpc'] + format_option + ['playlist'] , stdout=subprocess.PIPE)
        rows = res.stdout.decode('utf-8').splitlines()

        playlist = []
        for row in rows:
            split = row.split('\t')
            if len(split) == 5:
                playlist.append({
                    'position': split[0],
                    'title': split[1],
                    'artist': split[2],
                    'album': split[3],
                    'file': split[4],
                })
            else:
                playlist.append({
                    'position': "",
                    'title': "",
                    'artist': "",
                    'album': "",
                    'file': "",
                })

        return playlist

    def get_playlist_list(self):
        res = subprocess.run(['mpc'] + format_option + ['lsplaylist'] , stdout=subprocess.PIPE)
        playlists = res.stdout.decode('utf-8').splitlines()
        return playlists

    def toggle_play(self):
        res = subprocess.run(['mpc'] + format_option + ['toggle'] , stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def next(self):
        res = subprocess.run(['mpc'] + format_option + ['next'] , stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def prev(self):
        res = subprocess.run(['mpc'] + format_option + ['prev'] , stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def play_position(self, position):
        res = subprocess.run(['mpc'] + format_option + ['play', str(position)] , stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def volume(self, volume):
        res = subprocess.run(['mpc'] + format_option + ['volume', str(volume)] , stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def playlist_select(self, playlist_name):
        res = subprocess.run(['mpc'] + format_option + ['load', playlist_name] , stdout=subprocess.PIPE)
        return res.returncode == 0

    def crop(self):
        res = subprocess.run(['mpc'] + format_option + ['crop'] , stdout=subprocess.PIPE)
        return res.returncode == 0

    def queue_add(self, path):
        res = subprocess.run(['mpc', 'add', path] , stdout=subprocess.PIPE)
        return res.returncode == 0

    def set_player_mode(self, mode, state):
        if not mode in ['single', 'consume', 'random', 'repeat']:
            return None

        res = subprocess.run(['mpc'] + format_option + [mode, str(bool(state))] , stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def fetch_musicdir(self):
        response_dict = dict()
        res = subprocess.run(['mpc', 'listall'] , stdout=subprocess.PIPE)
        for row in res.stdout.decode('utf-8').splitlines():
            dirlist = row.split('/')
            filename = dirlist.pop()
            ld =  {'files': [filename]}
            for entry in reversed(dirlist):
                ld = {entry: ld}
            nestedupdate(ld,response_dict)

        return response_dict

    def reset_sleeptimer(self):
        subprocess.run(['pkill' , 'sleep'])
        subprocess.Popen([ self.mochi_dir + '/sleep.sh', '&'])

        res = subprocess.run(['mpc'] + format_option + ['status'] , stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def cancel_sleeptimer(self):
        subprocess.run(['pkill' , 'sleep'])

        res = subprocess.run(['mpc'] + format_option + ['status'] , stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

