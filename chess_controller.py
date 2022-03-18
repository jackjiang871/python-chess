from flask import (
    Blueprint, render_template, request, Response
)
import chess
import json

bp = Blueprint('chess_controller', __name__)

@bp.route('/update-board', methods=(['POST']))
def index():
    # require r1, c1, r2, c2, board, turn
    req_params = json.loads(request.json)
    required_params = ["r1", "c1", "r2", "c2", "board", "turn"]
    for param in required_params:
        if param not in req_params:
            return Response(status=404)

    # make sure params are numeric
    numeric_params = ["r1", "c1", "r2", "c2", "turn"]
    for numeric_param in numeric_params:
        if not req_params[numeric_param].isnumeric():
            return Response(status=404)
    
    # make sure board is a 8x8 2d list and all pieces are chess pieces
    board = req_params["board"]
    all_pieces = chess.get_black_pieces() + chess.get_white_pieces()
    if len(board) != 8:
        return Response(status=404)
    for row in board:
        if len(row) != 8:
            return Response(status=404)
        for piece in row:
            if piece not in all_pieces:
                return Response(status=404)
    

    next_board = chess.get_updated_board_if_is_valid_move(req_params["r1"], req_params["c1"], req_params["r2"], req_params["c2"], req_params["board"], req_params["turn"])

    return {"next_board": next_board}
