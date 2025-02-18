from flask import Flask
from flask import render_template


PATH_TO_OPENRADIOSS_DIR = "../OpenRadioss/"

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('main.html')

@app.route("/vtk")
def vtk():
    return render_template('vtk.html')