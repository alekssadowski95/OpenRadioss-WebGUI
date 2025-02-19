from flask import Flask
from flask import render_template


PATH_TO_OPENRADIOSS_DIR = "../OpenRadioss/"
INPUT_FILE = None

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('main.html')

@app.route("/vtk")
def vtk():
    return render_template('vtk.html')

@app.route("/set-inp-file")
def set_inp_file():
    return render_template('inp-upload.html')