from app import app, db
import os
from app.models import User
from random import randint
from datetime import datetime
import plotly.express as px
import plotly.io as pio
import pandas as pd


def fill_projects(num):
    for i in range(num):
        project = GPT(user_id=0, timestamp=datetime.utcnow(), observation="thisistheobs.",
                      integer_data=randint(1,530), boolean_data=True,
                      float_data=0.2)
        try:
            db.session.add(project)
        except:
            print("borking")
            return
    db.session.commit()


def retrieve_projects(user_id):
    '''retrieves all projects for a given user'''
    table = GPT.query.all()
    x = []
    y = []
    for entry in table:
        y.append(entry.integer_data)
        x.append(entry.id)
    data = [x,y]
    return data


def write_new_plot(plotfig, current_user, file_title, offline_capable=True, standalone=True):
    '''writes the plot to an html file, either standalone, or div tagged to be embedded later.
    offline_capable = true increases the file size by 3mb.
    offline_capable = False will make 3mb smaller, but require an internet connection to be used.
    https://plotly.github.io/plotly.py-docs/generated/plotly.io.write_html.html'''
    if offline_capable == False:
        offline_capable = 'CDN'
    if file_title[-5:] != '.html':
        file_title += '.html'
    cwd = os.path.join(os.getcwd(), 'userfiles')
    cwd = os.path.join(cwd, current_user)
    if not os.path.isdir(cwd):
        os.mkdir(cwd)
    file_path = os.path.join(cwd, file_title)
    pio.write_html(fig, file=file_path, auto_open=True) # , include_plotlyjs=offline_capable, full_html=standalone)
    return file_path


data = retrieve_projects(9)
fig = px.scatter(y=data[1], x=data[0])
fig.update_layout(template='plotly_white')
fig.update_layout(title='bigOLgraph')
write_new_plot(fig, 'userMCuserFace', 'BigOlTitle')