from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import DATA, UploadSet


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

datafiles = UploadSet('datafiles', DATA)

# This import causes errors if it is at the top of the file
from app import routes, models, errors, privatefunctions
