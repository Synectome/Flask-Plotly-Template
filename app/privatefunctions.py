'''
Stores backend functions to use in other modules without confusing
what those spaces are intended for
'''
import os
import time
import shutil
from app import app, db
from app.models import User


def user_directory_init(username):
    '''Only called once when user registers.
    creates a folder in the /userfiles for their plotly plots
    and data queries to be made'''

    cwd = os.path.join(os.getcwd(), 'app')
    cwd = os.path.join(cwd, 'userfiles')
    if not os.path.exists(cwd):
        os.mkdir(cwd)
    cwd = os.path.join(cwd, username)
    if not os.path.exists(cwd):
        os.mkdir(cwd)
    return cwd


def project_directory_string(project_name):
    '''generates the project directory path as a string'''
    cwd = os.path.join(os.getcwd(), 'app')
    cwd = os.path.join(cwd, 'projectfiles')
    cwd = os.path.join(cwd, project_name)
    return str(cwd)


def project_directory_init(project_name):
    '''Only called once when user creates the project.
    creates a folder in the app/projectfiles directory'''

    cwd = os.path.join(os.getcwd(), 'app')
    cwd = os.path.join(cwd, 'projectfiles')
    if not os.path.exists(cwd):
        os.mkdir(cwd)
    cwd = os.path.join(cwd, project_name)
    if not os.path.exists(cwd):
        os.mkdir(cwd)
        return cwd
    return 'Project Directory Already Exists. This project has been made already.'


def move_upload_to_secure_directory(username, filename, user_or_proj, project=None):
    '''Moves uploaded file from temp_uploads directory to either
    the users personal folder, or to a project directory.'''

    cwd = app.config['UPLOADS_DEFAULT_DEST']
    cwd = os.path.join(cwd, 'datafiles')
    filepath = os.path.join(cwd, filename)
    cwd = os.getcwd()

    if user_or_proj == '1':
        # project is a projectname,
        cwd = os.path.join(cwd, 'app')
        cwd = os.path.join(cwd, 'projectfiles')
        destination = os.path.join(cwd, project)
        if not os.path.exists(destination):
            os.mkdir(destination)
        destination = os.path.join(destination, filename)
    elif user_or_proj == '0':
        # upload to the users personal directory
        cwd = os.path.join(cwd, 'app')
        cwd = os.path.join(cwd, 'userfiles')
        destination = os.path.join(cwd, username)
        destination = os.path.join(destination, filename)
        print('filepath is :')
        print(str(filepath))
        print('destination is :')
        print(str(destination))
    else:
        return 'fat error with radio button tech'
    try:
        shutil.move(filepath, destination)
    except:
        print('shutil had error')
        return 'shutil.move had an error'

    # shutil.move worked, now delete the old file
    # os.remove(filepath)


def user_list():
    '''querys the User table to generate options
    as a list of (value, label) pairs, to be used in the choices argument of
    radio and select fields in forms'''
    # '<User {}>' ~> the user __repr__
    username = User.query.all()
    username_list = []
    # takes each user__repr__, splits by the space, then splits by the >, returns only the username
    for user in username:

        name = str(user)
        username_list.append((user.id, name.split()[1].split('>')[0]))
    return username_list


    # key_name_pairs = []
    # for i in range(len(username_list)):
    #     pair = (username_list[i], username_list[i])
    #     key_name_pairs.append(pair)
    # return key_name_pairs

def generate_users():
    for i in range(10):
        name = 'user' + str(i)
        email = name + '@user.com'
        password = 'pipilongtalking'

