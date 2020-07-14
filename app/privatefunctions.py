'''
Stores backend functions to use in other modules without confusing
what those spaces are inteded for
'''
import os


def user_directory_init(username):
    '''Only called once when user registers.
    creates a folder in the /userfiles for their plotly plots
    and data queries to be made'''

    cwd = os.path.join(os.getcwd(), 'userfiles')
    cwd = os.path.join(cwd, username)
    os.mkdir(cwd)
    return cwd

