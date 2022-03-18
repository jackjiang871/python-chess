from flask import (
    Blueprint, render_template, request, Response
)
import chess
import json

bp = Blueprint('chess_controller', __name__)

@bp.route('/update-board', methods=(['POST']))
def index():
    # require r1, c1, r2, c2, board, turn
    print(request.json)
    req_params = request.json
    required_params = ["r1", "c1", "r2", "c2", "board", "turn"]
    for param in required_params:
        if param not in req_params:
            return Response(response="missing param", status=404)

    # make sure params are numeric
    numeric_params = ["r1", "c1", "r2", "c2", "turn"]
    for numeric_param in numeric_params:
        if not isinstance(req_params[numeric_param], int) and not req_params[numeric_param].isnumeric():
            return Response(response="not numeric", status=404)
    
    # make sure board is a 8x8 2d list and all pieces are chess pieces
    board = req_params["board"]
    all_pieces = chess.get_black_pieces() + chess.get_white_pieces() + [" "]
    if len(board) != 8:
        return Response(response="bad board", status=404)
    for row in board:
        if len(row) != 8:
            return Response(response="bad board length", status=404)
        for piece in row:
            if piece not in all_pieces:
                return Response(response="bad board piece", status=404)
    r1 = int(req_params["r1"])
    c1 = int(req_params["c1"])
    r2 = int(req_params["r2"])
    c2 = int(req_params["c2"])
    turn = int(req_params["turn"])

    next_board = chess.get_updated_board_if_is_valid_move(r1, c1, r2, c2, req_params["board"], turn)

    return {"next_board": next_board}
