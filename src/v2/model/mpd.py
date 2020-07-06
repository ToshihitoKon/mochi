import subprocess
import regex
import pathlib

format_option = ['-f', '%position%\t%title%\t%artist%\t%album%\t%file%']

class Mpd:
    is_playing = False
    title = ''
    artist = ''
    playlist_pos = -1
    album = ''
    filepath = ''
    volume = -1
    duration = -1
    total = -1
    progress = -1
    repeat = False
    random = False
    single = False
    consume = False
    
    def parse_mpc_output(self, output):
        if output.find('ERROR') != -1:
            print("error: ", output)
            return False

        rows = output.splitlines()
        if len(rows) == 1:
            # song not set
            self.title = ''
            self.artist = ''
            self.is_playing = False
            status_line = rows[0]
        elif len(rows) == 3:
            # song set
            song_line = rows[0].split('\t')
            self.playlist_pos = song_line[0]
            self.title = song_line[1]
            self.artist = song_line[2]
            self.album = song_line[3]
            self.filepath =  song_line[4]

            player_line = rows[1]
            self.is_playing = (player_line.find('playing') != -1)
            song_length =  regex.search(r'(?P<dur>\d+:\d+)/(?P<tot>\d+:\d+).*\((?P<pro>\d+)%\)', player_line)
            self.progress = song_length.group('pro')

            split_duration = song_length.group('dur').split(':')
            self.duration = int(split_duration[0])*60 + int(split_duration[1])
            split_total = song_length.group('tot').split(':')
            self.total = int(split_total[0])*60 + int(split_total[1])


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
            self.volume = int(volume)
        else:
            self.volume = -1

        self.repeat = status_match.group('rep') == "on"
        self.random = status_match.group('ran') == "on"
        self.single = status_match.group('sin') == "on"
        self.consume = status_match.group('con') == "on"
        return True

    def status_object(self):
        return {
                'isplaying': self.is_playing,
                'artist': self.artist,
                'title': self.title,
                'playlist_position': self.playlist_pos,
                'album': self.album,
                'filepath': self.filepath,
                'duration': self.duration,
                'total': self.total,
                'progress': self.progress,
                'volume': self.volume,
                'repeat': self.repeat,
                'random': self.random,
                'single': self.single,
                'consume': self.consume
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
            playlist.append({
                'position': split[0],
                'title': split[1],
                'artist': split[2],
                'album': split[3],
                'file': split[4],
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
        print(res.args)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def playlist_select(self, playlist_name):
        res = subprocess.run(['mpc'] + format_option + ['load', playlist_name] , stdout=subprocess.PIPE)
        return res.returncode == 0

    def crop(self):
        res = subprocess.run(['mpc'] + format_option + ['crop'] , stdout=subprocess.PIPE)
        return res.returncode == 0

    def set_player_mode(self, mode, state):
        if not mode in ['single', 'consume', 'random', 'repeat']:
            return None

        res = subprocess.run(['mpc'] + format_option + [mode, str(bool(state))] , stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def list_musicdir(self, path):
        mpd_music_dir = '/var/lib/mpd/music'
        entries = []
        listpath = pathlib.Path(mpd_music_dir).joinpath(path)
        if not listpath.is_dir():
            return None
        for p in list(listpath.iterdir()):
            if p.is_dir():
                entries.append({'path': str(p.relative_to(mpd_music_dir)), 'type': 'dir'})
            else:
                entries.append({'path': str(p.relative_to(mpd_music_dir)), 'type': 'file'})
        return entries

if __name__ == '__main__':
    mpd = Mpd()
    print(mpd.list_musicdir(''))
