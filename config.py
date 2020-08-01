import os
basedir = os.path.abspath(os.path.dirname(__file__))
app_dir = os.path.join(basedir, 'app')


class Config(object):
    FLASK_DEBUG = 1
    # security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # uploading files
    UPLOADED_FILES_DEST = os.path.join(app_dir, 'uploads_temp')
    UPLOADED_FILES_DENY = {'php'}
    UPLOAD_MAX_SIZE = 5e+8 # no max file size used yet.
    ALLOWED_EXTENSIONS = {'csv', 'json'} # not used as of july 15, using flask_uploads.DATA for this purpose
    UPLOADS_DEFAULT_DEST = os.path.join(app_dir, 'uploads_temp')

    # For Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
