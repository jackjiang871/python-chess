from flask import (
    Blueprint, render_template, request
)
import chess

bp = Blueprint('chess_controller', __name__)

@bp.route('/next-board', methods=(['GET']))
def index():
    # chess.get_updated_board_if_is_valid_move()
    request.args.get("r1")
    return render_template('base.html')