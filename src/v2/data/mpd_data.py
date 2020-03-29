import os

class MpdStatusData:
    is_playing = False
    title = ''
    artist = ''
    volume = 0
    repeat = False
    random = False
    single = False
    consume = False
    
    def set_status(self, is_playing, title, artist, volume, repeat, random, single, consume):
        self.is_playing = is_playing
        self.title = title
        self.artist = artist
        self.volume = volume
        self.repeat = repeat
        self.random = random
        self.single = single
        self.consume = consume

    def get_status(self):
        return 'dummy status'

    def get_playlist(self):
        return 'dummy playlist'

class MpdPlaylistData:
    title = ''
    artist = ''
    path = ''
    entry = 0
    def __init__(self, title, artist, path, entry):
        self.title = title
        self.artist = artist
        self.path = path
        self.entry = entry

    
if __name__ == '__main__':
    mpd_data = MpdData()
    print(mpd_data.get_status())
    print(mpd_data.get_playlist())
