from flask import Flask
import chess

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"