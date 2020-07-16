import time
from app import app, db, datafiles
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, UploadForm, NewProjectForm
from app.models import User, Project
from app.privatefunctions import user_directory_init, project_directory_init, \
    move_upload_to_secure_directory as move_upload
from flask_uploads import configure_uploads
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    '''This is the index page view function.'''
    # user = {'username':'admin'}
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user_directory_init(form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

##################################################################
# -----------------FILE UPLOAD SECTION-------------------------- #
##################################################################


configure_uploads(app, datafiles)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        filedata = form.file.data
        print('here comes the project_name')
        print(form.project_name.data)
        print('here comes the radio selection')
        print(form.project_or_user.data)
        if form.project_or_user == '1' and form.project_name == '':
            return redirect(url_for('upload')), flash('Project destination selected, but no project name given.')
        if secure_filename(filedata.filename):
            saved = datafiles.save(filedata)
            time.sleep(3)
            move_upload(current_user.username, filedata.filename, form.project_or_user.data,
                        project=form.project_name.data)
            return redirect(url_for('index')), flash('upload successful')
        else:
            return redirect(url_for('upload')), flash('insecure filename, please rename file before uploading.')
    print(form.errors)
    return render_template('upload.html', form=form)


##################################################################
# --------------------PROJECT CREATION-------------------------- #
##################################################################
@app.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    form = NewProjectForm()
    if form.validate_on_submit():
        project = Project(title=form.project_title.data, description=form.description.data)
        #Check that the project name doesn't already exist

        #user_directory_init(form.username.data)
        #user.set_password(form.password.data)
        #db.session.add(user)
        #db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('new_project.html', title='New Project', form=form)


##################################################################
# -------------------PLOTTING and DATA-------------------------- #
##################################################################
@app.route('/vis')
def vis():
    return render_template('vis.html', title='graph vis')

