import subprocess
import regex

format_option = ['-f', '%position%\t%title%\t%artist%\t%album%\t%file%']

class Mpd:
    is_playing = False
    title = ''
    artist = ''
    volume = 0
    position = ''
    length = ''
    progress = 0
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
            self.title = song_line[1]
            self.artist = song_line[2]

            player_line = rows[1]
            self.is_playing = (player_line.find('playing') != -1)
            position_length =  regex.search(r'(?P<pos>\d+:\d+)/(?P<len>\d+:\d+).*\((?P<per>\d+)%\)', player_line)
            self.position = position_length.group('pos')
            self.length = position_length.group('len')
            self.progress = position_length.group('per')

            status_line = rows[2]
        else:
            return False

        status_match = regex.search(
                r'volume:\s+(?<vol>[^\s]+)\s+'
                'repeat:\s+(?<rep>[^\s]+)\s+'
                'random:\s+(?<ran>[^\s]+)\s+'
                'single:\s+(?<sin>[^\s]+)\s+'
                'consume:\s+(?<con>[^\s]+).*', status_line)

        if status_match.group('vol').isdecimal():
            self.volume = int(status_match.group('vol'))
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
                'position': self.position,
                'total': self.length,
                'progress': self.progress,
                'volume': self.volume,
                'repeat': self.repeat,
                'random': self.random,
                'single': self.single,
                'consume': self.consume
        }

    def get_status(self):
        res = subprocess.run(['mpc', 'status'] + format_option, stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()


    def get_playlist(self):
        res = subprocess.run(['mpc', 'playlist'] + format_option, stdout=subprocess.PIPE)
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
        res = subprocess.run(['mpc', 'lsplaylist'], stdout=subprocess.PIPE)
        playlists = res.stdout.decode('utf-8').splitlines()
        return playlists

    def toggle_play(self):
        res = subprocess.run(['mpc', 'toggle'] + format_option, stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def next(self):
        res = subprocess.run(['mpc', 'next'] + format_option, stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def prev(self):
        res = subprocess.run(['mpc', 'prev'] + format_option, stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def volume(self, volume):
        res = subprocess.run(['mpc', 'volume', volume] + format_option, stdout=subprocess.PIPE)
        if not self.parse_mpc_output(res.stdout.decode('utf-8')):
            return None
        return self.status_object()

    def playlist_select(self, playlist_name):
        res = subprocess.run(['mpc', 'load', playlist_name] + format_option, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode == 0

if __name__ == '__main__':
    mpd = Mpd()
    print(mpd.playlist_select('a'))
