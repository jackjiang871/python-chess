from flask import Flask
from flask_cors import CORS

from flask import Blueprint

bp = Blueprint('chess_controller', __name__)

import routes.create_user
import routes.get_players
import routes.health_check
import routes.update_board

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    CORS(app)
    return app