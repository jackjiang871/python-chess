from flask import Flask

def create_app():
    app = Flask(__name__)
    import chess_controller
    app.register_blueprint(chess_controller.bp)
    return app