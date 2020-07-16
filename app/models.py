from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader # not a part of any classes
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # generic_project = db.relationship('GenericProjectTable', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


project_members = db.Table('members',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')), # user must be lower case
                           db.Column('project_id', db.Integer, db.ForeignKey('projects.id'))) # projects must be lower2


class Projects(db.Model):
    '''SQL TABLE: list of projects
        id = int
        title = string(100)
        description = string(300)
        project_files_path = string(300)
        members = many-many relationship through 'project_members' '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(300))
    project_files_path = db.Column(db.String(300))
    members = db.relationship('User', secondary=project_members,
                              primaryjoin=(project_members.c.user_id == id),
                              secondaryjoin=(project_members.c.project_id == id),
                              backref=db.backref('project_members', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '''project id : {}
        title : {}
        description : {}
        file path : {}
        members : {}'''.format(self.id, self.title, self.description, self.project_files_path, self.members)


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
