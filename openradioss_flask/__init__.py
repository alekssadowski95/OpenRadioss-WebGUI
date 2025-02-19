import os

from flask import Flask
from flask import render_template, redirect, url_for, session

from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import SubmitField

from .inp2rad import start as convert_inp_to_rad


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

@app.route("/", methods = ["GET", "POST"])
def home():
    form = UploadForm()
    if form.validate_on_submit():
        # Get the file from the form
        file = form.upload.data

        # Generate a safe filename (you can adjust naming as needed)
        filename = file.filename

        # Save the file to the designated upload folder
        full_file_path = os.path.join(app.config['APP_PATH'], app.config['UPLOAD_FOLDER'], filename)
        file.save(full_file_path)
        session['current_inp_path'] = full_file_path

        # Print a success message
        print(f'File {filename} uploaded successfully!', 'success')
        
        return redirect(url_for('read_calculix_input'))
    return render_template('main.html', form = form)

@app.route("/create-rad-input")
def create_rad_input():
    convert_inp_to_rad(session['current_inp_path'])
    return redirect('read_rad_input')

@app.route("/create-rad-anim")
def create_rad_anim():
    return redirect('read_rad_anim')

@app.route("/create-vtk-anim")
def create_vtk_anim():
    return redirect('read_vtk_anim')

@app.route("/read-calculix-input")
def read_calculix_input():
    full_file_path = session['current_inp_path']
    inp_file_content = "Not loaded"
    with open(full_file_path, 'r') as file:
        inp_file_content = file.read()
    return render_template('file.html', content = inp_file_content)

@app.route("/read-rad-input")
def read_rad_input():
    rad_inp_content = "No rad input deck"
    return render_template('file.html', content = rad_inp_content)

@app.route("/read-rad-anim")
def read_rad_anim():
    rad_anim_content = "No rad animation"
    return render_template('file.html', content = rad_anim_content)

@app.route("/read-vtk-anim")
def read_vtk_anim():
    vtk_anim_content = "No vtk animation"
    return render_template('file.html', content = vtk_anim_content)
