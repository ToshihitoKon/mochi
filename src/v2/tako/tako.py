import flask
import os

class Model:
    def __init__(self, config):
        self.config = config
        self.row_dir = config.must('MOCHI_TAKO_RAW_ROOT')
        self.thumbnail_dir = config.must('MOCHI_TAKO_THUMBNAIL_ROOT')

    def save_file(self, data):
        filename = data.filename
        if filename == '':
            return False

        data.save(os.path.join(self.raw_dir, filename))
        return True

    def list_file(self):
        ls = os.listdir(self.raw_dir)
        return [x for x in ls if x != 'thumbnail']

    def serve_file(self, path):
        try:
            return flask.send_file(os.path.join(self.raw_dir, path), \
                    as_attachment=False)
        except:
            return False

def get_model(config):
    return Model(config)
        
if __name__ == "__main__":
    print(Model().list_file())
