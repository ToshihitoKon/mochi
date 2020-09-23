import flask
import os

save_dir = os.path.expanduser('~/tako')
class Tako:
    def save_file(self, data):
        filename = data.filename
        if filename == '':
            return False

        data.save(os.path.join(save_dir, filename))
        return True

    def list_file(self):
        ls = os.listdir(save_dir)
        return [x for x in ls if x != 'thumbnail']

    def serve_file(self, path):
        try:
            return flask.send_file(os.path.join(save_dir, 'thumbnail', path), \
                    as_attachment=False)
        except:
            return False
        
if __name__ == "__main__":
    print(Tako().list_file())
