from flask import Flask
from flask import render_template
import webview


app = Flask(__name__)
window = webview.create_window('OpenRadioss', app)

@app.route("/")
def hello_world():
    return render_template('main.html')