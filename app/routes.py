import time
from app import app, db, datafiles
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, UploadForm, NewProjectForm, ProjectPermissionsForm
from app.models import User, Project, ProjectMembers #project_members
from app.privatefunctions import user_directory_init,project_directory_init, \
    move_upload_to_secure_directory as move_upload, project_directory_string, user_list
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
        db.session.expire_all()
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
def user_getter(ids):
    users = []
    for ident in ids:
        users.append(User.query.filter_by(id=ident).first())
    if current_user.id not in ids:
        users.append(current_user)
    return users


@app.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    form = NewProjectForm()
    form.members_picks.choices = [(person.id, person.username) for person in User.query.all()]
    if form.validate_on_submit():
        path = project_directory_string(form.project_title.data)
        membs = user_getter(form.members_picks.data)
        project = Project(title=form.project_title.data, description=form.description.data,
                          project_files_path=path, creator=current_user)
        db.session.add(project)
        db.session.commit() # appears to work fine.
        project_directory_init(form.project_title.data)
        project = most_recent_project(current_user.id)

        for member in membs:
            db.session.add(ProjectMembers(id=None, user_id=member.id, project_id=project.id, permission=99))
            db.session.commit() # causes error
        flash('Project initiated successfully!')
        return redirect(url_for('project_permissions'))
    return render_template('new_project.html', title='New Project', form=form)


def most_recent_project(creator_id):
    x = Project.query.filter(Project.creator_id==current_user.id).order_by(Project.timestamp.desc()).first()
    print(x)
    return x


def id2name(id):
    return User.query.filter_by(id=id).first().username


def permission_writer(form, project_id, tablequery): # took out project.id
    current_project_entries = ProjectMembers.query.filter(ProjectMembers.id==project_id)
    for member_id in form.admin.data:
        current_project_entries.filter(ProjectMembers.user_id==member_id).update({ProjectMembers.permission: 2},
                                                                                 synchronize_session='evaluate')
    for member_id in form.readwrite.data:
        current_project_entries.filter(ProjectMembers.user_id == member_id).update({ProjectMembers.permission: 1},
                                                                                   synchronize_session='evaluate')
    for member_id in form.readonly.data:
        current_project_entries.filter(ProjectMembers.user_id == member_id).update({ProjectMembers.permission: 0},
                                                                                   synchronize_session='evaluate')
    db.session.commit()


@app.route('/project_permissions', methods=['GET', 'POST'])
@login_required
def project_permissions():
    project = most_recent_project(current_user.id)
    # db.session.query(project_members).filter(project_members.c.project_id== project_id_var).all()
    table_query = ProjectMembers.query.filter(ProjectMembers.id==project.id).all()
    # choices = [(person.user_id, id2name(person.user_id)) for person in table_query]
    choices = [(person.id, person.username) for person in project.members]
    form = ProjectPermissionsForm()
    form.admin.choices = choices
    form.readwrite.choices = choices
    form.readonly.choices = choices
    if form.validate_on_submit():
        permission_writer(form, project.id,  table_query)
        flash('Permissions successfully set!')
        return redirect(url_for('index'))
    return render_template('new_project.html', title=str(project.title) + " permissions", form=form)


##################################################################
# -------------------PLOTTING and DATA-------------------------- #
##################################################################
@app.route('/vis')
def vis():
    return render_template('vis.html', title='graph vis')

