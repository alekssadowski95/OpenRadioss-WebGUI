from flask import Flask
import webview


app = Flask(__name__)
window = webview.create_window('OpenRadioss', app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"