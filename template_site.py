from app import app, db
from app.models import User, Projects, UserPlots


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Projects': Projects, 'UserPlots': UserPlots}