from app import app, db
from app.models import User, Project, UserPlots, ProjectMembers


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Project': Project, 'UserPlots': UserPlots, 'ProjectMembers': ProjectMembers}
