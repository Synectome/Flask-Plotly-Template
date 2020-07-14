'''
Stores backend functions to use in other modules without confusing
what those spaces are intended for
'''
import os
import time
import shutil
from app import app


def user_directory_init(username):
    '''Only called once when user registers.
    creates a folder in the /userfiles for their plotly plots
    and data queries to be made'''

    cwd = os.path.join(os.getcwd(), 'userfiles')
    cwd = os.path.join(cwd, username)
    os.mkdir(cwd)
    return cwd


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
