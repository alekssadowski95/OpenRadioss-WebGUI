import os

from flask import Flask
from flask import render_template, redirect, url_for, session, jsonify, send_from_directory, send_file, session

from flask_cors import CORS

from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import SubmitField

from .inp2rad import start as convert_inp_to_rad

import psutil
import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import re
from typing import List, Tuple


paths_to_data = {
    "inp": None,
    "rad0000": None,
    "rad0001": None,
    "anim_list": [
        (1, "test", "test.vtk")
    ]
}

session['prcessing_thread'] = 0

app = Flask(__name__)

CORS(app)

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

@app.route("/data/<filename>")
def data(filename):
    filepath = os.path.join(app.config['APP_PATH'], app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath)

@app.route('/viewer/<filename>')
def viewer(filename):
    return render_template('viewer.html', filename = filename)

@app.errorhandler(404)
def not_found(e):
  return render_template('404_errorpage.html'), 404

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
        session['prcessing_thread'].join()

        # remove old simulation data
        remove_all_files_in_directory(os.path.join(app.config['APP_PATH'], 'data'))

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

        observer_thread = threading.Thread(target = start_observer).start()
        session['prcessing_thread'] = threading.Thread(target = process_calculix_inp, args = (inp_file_path, observer_thread, )).start()


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
            if os.path.isfile(os.path.join(directory, f)):
                if f.endswith('.vtk'):
                    result.append((1, f))
                    """
            if os.path.isfile(os.path.join(directory, f)) and '.' not in f:
                match = re.search(r'\d{3}$', f)
                if match:
                    result.append((match.group(0), f))"
                    """
        return result
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied for accessing '{directory}'.")
        return []

def process_calculix_inp(inp_path, observer_thread):    
    convert_inp_to_rad(inp_path)
    run_openradioss()
    observer_thread.join()

@app.route("/get-result-list")
def get_result_list():
    anim_list = list_filenames(os.path.join(app.config['APP_PATH'], 'data'))
    return jsonify(anim_list)

@app.route("/get-single-result/<anim_name>")
def get_single_result(anim_name):
    uploads = os.path.join(app.config['APP_PATH'], 'data')
    return send_from_directory(uploads, anim_name)

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Check if the event is a file (not a directory)
        if event.is_directory:
            return 
        # Print the filename when a new file is created
        print(f'New file created: {os.path.basename(event.src_path)}')
        
        if is_rad_anim_filename(os.path.basename(event.src_path)) and not os.path.basename(event.src_path).endswith("A001"):
            # Extract directory and filename
            dir_name, base_name = os.path.split(str(event.src_path))
            
            # Regex to match the pattern (e.g., 'bulletA002')
            match = re.search(r'(.*?)(\d+)$', base_name)
            if not match:
                raise ValueError("Filename does not match the expected pattern")
            
            prefix, num_part = match.groups()
            new_num = str(int(num_part) - 1).zfill(len(num_part))  # Preserve leading zeros
            new_filename = f"{prefix}{new_num}"

            new_filepath = os.path.join(dir_name, new_filename)

            # start thread
            threading.Thread(target = create_vtk_anim, args = (new_filepath, )).start()

def create_vtk_anim(rad_anim_path):
    import subprocess
    print(str(os.path.join(app.config['OPENRADIOSS_PATH'], 'exec', 'anim_to_vtk_win64.exe') + " " + rad_anim_path + " > " + os.path.basename(rad_anim_path) + ".vtk"))
    subprocess.call(str(os.path.join(app.config['OPENRADIOSS_PATH'], 'exec', 'anim_to_vtk_win64.exe') + " " + rad_anim_path + " > " + os.path.basename(rad_anim_path) + ".vtk"), stdout=subprocess.PIPE, shell=True)
    print('Created file: ' + os.path.basename(rad_anim_path) + ".vtk")

def start_observer():
    observer = Observer()
    my_handler = MyHandler()
    observer.schedule(my_handler, path=os.path.join(app.config['APP_PATH'], 'data'), recursive=False)
    observer.start()

def is_rad_anim_filename(s: str) -> bool:
    # Regular expression to check if the string ends with 'A' followed by 3 digits
    pattern = r"A\d{3}$"
    
    # Check if the string matches the pattern
    return bool(re.search(pattern, s))

def remove_all_files_in_directory(directory: str):
    # Iterate over all the files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Check if it is a file and not a directory
        if os.path.isfile(file_path):
            os.remove(file_path)  # Remove the file
            print(f'Removed file: {file_path}')










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
