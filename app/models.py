from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# many to many with a model based association table for relationship data
#   https://stackoverflow.com/questions/30406808/flask-sqlalchemy-difference-between-association-model-and-association-table-fo

# project_members = db.Table('members',
#                            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                            db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
#                            db.Column('permission', db.Integer)) # 0 = r, 1 = rw, 2 = rw & delete.


class ProjectMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #, primary_key=True) # having another primary key messed it
    project_id = db.Column(db.Integer, db.ForeignKey('project.id')) #, primary_key=True)
    permission = db.Column(db.Integer, nullable=True)
    user = db.relationship('User', backref=db.backref('Project'))
    project = db.relationship('Project', backref=db.backref('User'))

    def __repr__(self):
        return '''
        +----------------------------------------+
        + user_id : {}
        + project_id : {}
        + permission : {}'''.format(self.user_id, self.project_id, self.permission)


@login.user_loader # not a part of any classes
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    projects_created = db.relationship('Project', backref='creator')
    plots = db.relationship('UserPlots', backref='creator')
    member_of = db.relationship('Project', secondary=lambda: ProjectMembers.__table__)#, backref=db.backref('User', lazy='dynamic'))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    project_files_path = db.Column(db.String(300))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    members = db.relationship('User', secondary=lambda: ProjectMembers.__table__,
                              backref=db.backref('User', lazy='dynamic'))

    def __repr__(self):
        return '''project id : {}
        title : {}
        date : {}
        description : {}
        creator : {}
        file path : {}
        members : {}'''.format(self.id, self.title, self.timestamp, self.description, self.creator,
                               self.project_files_path, self.members)


class UserPlots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('User_id', db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column(db.String(100))
    notes = db.Column(db.String(300))
    plot_file_path = db.Column(db.String(300))

    def __repr__(self):
        return '''Plot ID : {}
        User : {}
        Plot Title : {}
        Date Created : {}
        Notes : {}
        File Path : {}'''.format(self.id, self.user_id, self.title, self.timestamp, self.notes,
                                 self.plot_file_path)


# class GenericProjectTable(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column('User_id', db.Integer, db.ForeignKey('user.id'))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     observation = db.Column(db.String(256))
#     integer_data = db.Column(db.Integer)
#     boolean_data = db.Column(db.Boolean)
#     float_data = db.Column(db.Float)
#
#     def __repr__(self):
#         return '''GenericProjectRecord:
#         project: {}
#         user: {}
#         time: {}
#         observation: {}
#         int data: {}
#         bool data: {}
#         float data: {}'''.format(self.id, self.user_id, self.timestamp, self.observation,
#                                           self.integer_data, self.boolean_data, self.float_data)
