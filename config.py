import os
basedir = os.path.abspath(os.path.dirname(__file__))
app_dir = os.path.join(basedir, 'app')


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(app_dir, 'uploads_temp')
    UPLOAD_MAX_SIZE = 5e+8
