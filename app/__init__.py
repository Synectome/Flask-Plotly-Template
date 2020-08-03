import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import DATA, UploadSet
from flask_bootstrap import Bootstrap
from flask_restless import APIManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler


class SQLiteAlchemy(SQLAlchemy):
    '''allows me to change the isolation level.
    source:  https://github.com/pallets/flask-sqlalchemy/issues/120'''
    def apply_driver_hacks(self, app, info, options):
        options.update({
            'isolation_level': 'READ COMMITTED',
        })
        super(SQLiteAlchemy, self).apply_driver_hacks(app, info, options)


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
datafiles = UploadSet('datafiles', DATA)
bootstrap = Bootstrap(app)
manager = APIManager(app, flask_sqlalchemy_db=db)

# miguel grinberg error logging
if not app.debug: # only run when debugging is disabled
    # Emailing file logger
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Flask-Template-Site Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    # Rotating File Logger (not emailing)
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/FullSite.log', maxBytes=20480,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask-Template-Site startup')

# This import causes errors if it is at the top of the file
from app import routes, models, errors, privatefunctions

# This prevents database upgrade error for sqlite in dev mode when droping a column during upgrade
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

# ----------------------------------------------- #
# ------------API-MANAGER-CREATION--------------- #
# ----------------------------------------------- #
api_denied_fields = ['email', 'password_hash']
# --User API--
manager.create_api(models.User, url_prefix='/rest/get/', methods=['GET'],
                   preprocessors=dict(GET_SINGLE=[routes.auth_func], GET_MANY=[routes.auth_func]),
                   exclude_columns=api_denied_fields)
manager.create_api(models.User, url_prefix='/rest/add/', methods=['POST'],
                   preprocessors=dict(GET_SINGLE=[routes.auth_func], GET_MANY=[routes.auth_func]),
                   exclude_columns=api_denied_fields)
manager.create_api(models.User, url_prefix='/rest/update/', methods=['PATCH'],
                   preprocessors=dict(GET_SINGLE=[routes.auth_func], GET_MANY=[routes.auth_func]),
                   exclude_columns=api_denied_fields)
# manager.create_api(User, url_prefix='/rest/delete/users/', methods=['DELETE'],
#                   preprocessors = dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func]),
#                   exclude_columns=api_denied_fields) # To Dangerous to have enabled  as is
# --Project API--
manager.create_api(models.Project, url_prefix='/rest/get/', methods=['GET'],
                   preprocessors=dict(GET_SINGLE=[routes.auth_func], GET_MANY=[routes.auth_func]),
                   exclude_columns=api_denied_fields)