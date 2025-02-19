import os

from flask import Flask
from flask import render_template, redirect, url_for, session

from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import SubmitField

from .inp2rad import start as convert_inp_to_rad

import psutil


'''
1. Upload calculix input
2. Create rad input deck (0000, 0001)
3. Create rad animation
4. Create vtk animation
'''


app = Flask(__name__)

# Define the path for the app
app.config['APP_PATH'] = os.path.dirname(os.path.abspath(__file__))
print(app.config['APP_PATH'])

# Define upload folder name
app.config['UPLOAD_FOLDER'] = "data"

app.config['OPENRADIOSS_PATH'] = os.path.join(os.path.dirname(app.config['APP_PATH']), "OpenRadioss_libs")
print(app.config['OPENRADIOSS_PATH'])

app.config['CORE_COUNT'] = psutil.cpu_count(logical=False)

'''
session["current_inp_path"] = "No input file"
session["current_rad_0001_path"] = "No rad0001 file"
session["current_rad_0002_path"] = "No rad0002 file"
session["current_rad_anim_paths"] = ["No rad anim files"]
session["current_vtk_anim_paths"] = ["No vtk anim files"]
'''

# Add secret key
app.config['SECRET_KEY'] = 'afs87fas7bfsa98fbasbas98fh78oizu'

class UploadForm(FlaskForm):
    upload = FileField('image', validators=[FileRequired(),])
    submit = SubmitField('Upload')

@app.route("/")
def home():
    return redirect(url_for('upload_calculix_input'))

@app.route("/upload-calculix-input", methods = ["GET", "POST"])
def upload_calculix_input():
    form = UploadForm()
    content = "No calculix input"
    try:
        if session.get('current_inp_path'):
            with open(session['current_inp_path'], 'r') as file:
                content = file.read()
    except:
        pass
    if form.validate_on_submit():
        # clear session
        session['current_inp_path'] = None
        session['current_rad_inp_paths'] = None
        session['current_log_paths'] = None
        session['current_rad_anim_paths'] = None
        session['current_vtk_anim_paths'] = None

        # Get the file from the form
        file = form.upload.data

        # Generate a safe filename (you can adjust naming as needed)
        filename = file.filename

        # Save the file to the designated upload folder
        inp_file_path = os.path.join(app.config['APP_PATH'], app.config['UPLOAD_FOLDER'], filename)
        file.save(inp_file_path)
        session['current_inp_path'] = inp_file_path

        rad_inp_file_paths = create_rad_input(inp_file_path)
        rad_anim_file_paths = run_openradioss(rad_inp_file_paths)
        vtk_anim_paths = create_vtk_anim(rad_anim_file_paths)
        
        return redirect(url_for('read_result'))
    return render_template('upload.html', form = form, content = content, onfig = app.config)

@app.route("/read-result")
def read_result():
    content = "No result"
    return render_template('file.html', content = content, config = app.config)

@app.route("/read-logs")
def read_logs():
    content = "No logs"
    return render_template('file.html', content = content, config = app.config)

def create_rad_input():
    current_inp_path = session['current_inp_path']
    current_inp_path_wo_ext = os.path.splitext(current_inp_path)[0]
    convert_inp_to_rad(current_inp_path)
    return (current_inp_path_wo_ext + "_0000.rad", current_inp_path_wo_ext + "_0001.rad")

def run_openradioss():
    pass

def create_vtk_anim():
    pass













'''
Not now
'''
@app.route("/create-rad-anim")
def create_rad_anim():
    return redirect('read_rad_anim')

@app.route("/create-vtk-anim")
def create_vtk_anim():
    return redirect('read_vtk_anim')

@app.route("/read-rad-input")
def read_rad_input():
    content = "No rad input deck"
    try:
        if session.get('current_rad_inp_paths'):    
            with open(session['current_rad_inp_paths'][0], 'r') as file_0:
                content = file_0.read()
            with open(session['current_rad_inp_paths'][1], 'r') as file_1:
                content = content + (file_1.read())
    except:
        pass
    return render_template('file.html', content = content, config = app.config)

@app.route("/read-rad-log")
def read_rad_log():
    content = "No rad log"
    return render_template('file.html', content = content, config = app.config)

@app.route("/read-rad-anim")
def read_rad_anim():
    content = "No rad animation"
    try:
        if session.get('current_rad_anim_paths'):
            pass
    except:
        pass
    return render_template('file.html', content = content, config = app.config)

@app.route("/read-vtk-anim")
def read_vtk_anim():
    content = "No vtk animation"
    try:
        if session.get('current_vtk_anim_paths'):
            pass
    except:
        pass
    return render_template('file.html', content = content, config = app.config)
