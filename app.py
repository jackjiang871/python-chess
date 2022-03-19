from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    import chess_controller
    app.register_blueprint(chess_controller.bp)
    CORS(app)
    return app