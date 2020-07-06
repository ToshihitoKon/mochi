import os

save_dir = os.path.expanduser('~/tako')
class Tako:
    def save_file(self, data):
        filename = data.filename
        if filename == '':
            return False

        data.save(os.path.join(save_dir, filename))
        return True
