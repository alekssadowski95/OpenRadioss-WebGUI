import os

from flask import Flask
from flask import render_template, redirect, url_for, session, jsonify, send_from_directory

from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import SubmitField

from .inp2rad import start as convert_inp_to_rad

import psutil
import threading


paths_to_data = {
    "inp": None,
    "rad0000": None,
    "rad0001": None,
    "anim_list": [
        (1, "test", "test.vtk")
    ]
}

app = Flask(__name__)

# Define the path for the app
app.config['APP_PATH'] = os.path.dirname(os.path.abspath(__file__))
print(app.config['APP_PATH'])

# Define upload folder name
app.config['UPLOAD_FOLDER'] = "data"

app.config['OPENRADIOSS_PATH'] = os.path.join(os.path.dirname(app.config['APP_PATH']), "OpenRadioss_libs")
print(app.config['OPENRADIOSS_PATH'])

app.config['CORE_COUNT'] = psutil.cpu_count(logical=False)

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
        # clear data
        paths_to_data["inp"] = None
        paths_to_data["rad0000"] = None
        paths_to_data["rad0001"] = None

        # Get the file from the form
        file = form.upload.data

        # Generate a safe filename (you can adjust naming as needed)
        filename = file.filename

        # Save the file to the designated upload folder
        inp_file_path = os.path.join(app.config['APP_PATH'], app.config['UPLOAD_FOLDER'], filename)
        file.save(inp_file_path)
        paths_to_data["inp"] = inp_file_path
        current_inp_path_wo_ext = os.path.splitext(inp_file_path)[0]
        paths_to_data["rad0000"] = current_inp_path_wo_ext + "_0000.rad"
        paths_to_data["rad0001"] = current_inp_path_wo_ext + "_0001.rad"

        threading.Thread(target = process_calculix_inp, args = (inp_file_path, )).start()

        return redirect(url_for('read_result'))
    return render_template('upload.html', form = form, content = content, onfig = app.config)

@app.route("/read-result")
def read_result():
    print(paths_to_data["rad0000"])
    content_0 = "No result"
    content_1 = "No result"
    calculix_inp = "No result"
    try:
        if paths_to_data["rad0000"]:    
            with open(paths_to_data["rad0000"], 'r') as file_0:
                content_0 = file_0.read()
            with open(paths_to_data["rad0001"], 'r') as file_1:
                content_1 = file_1.read()
            with open(paths_to_data["inp"], 'r') as file_2:
                calculix_inp = file_2.read()
    except:
        pass
    paths_to_data["anim_list"] = list_filenames(os.path.join(app.config['APP_PATH'], 'data'))
    return render_template('result.html', content_0 = content_0, content_1 = content_1, calculix_inp = calculix_inp, anim_list = paths_to_data["anim_list"], config = app.config)

@app.route("/read-logs")
def read_logs():
    content = "No logs"
    return render_template('file.html', content = content, config = app.config)

def run_openradioss():
    working_dir = os.path.join(app.config['APP_PATH'], 'data')
    os.chdir(working_dir)
    openradioss_path = os.path.join(os.path.dirname(app.config['APP_PATH']), 'OpenRadioss_libs')
    os.system("C:/Users/Work/Documents/Github/OpenRadioss2/run-openradioss.bat" + " " + working_dir + " " + openradioss_path + " " + "bullet")

import os
import re
from typing import List, Tuple

def list_filenames(directory: str) -> List[Tuple[str, str]]:
    """
    Returns a list of filenames that end with three numeric characters and have no file extension,
    along with the extracted number.

    :param directory: Path to the directory.
    :return: List of tuples (extracted number, filename) in the directory.
    """
    try:
        result = []
        for f in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, f)) and '.' not in f:
                match = re.search(r'\d{3}$', f)
                if match:
                    result.append((match.group(0), f))
        return result
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied for accessing '{directory}'.")
        return []

def create_vtk_anim():
    pass

def process_calculix_inp(inp_path):
    convert_inp_to_rad(inp_path)
    run_openradioss()
    create_vtk_anim()

@app.route("/get-result-list")
def get_result_list():
    anim_list = list_filenames(os.path.join(app.config['APP_PATH'], 'data'))
    return jsonify(anim_list)


@app.route("/get-single-result/<anim_name>")
def get_single_result(anim_name):
    uploads = os.path.join(app.config['APP_PATH'], 'data')
    return send_from_directory(uploads, anim_name)













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
