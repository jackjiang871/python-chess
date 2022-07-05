from app import bp, lock
from flask import (request, Response)
from utils import database

@bp.route('/make-move', methods=(['POST']))
def make_move():
    # require r1, c1, r2, c2, session_id
    req_params = request.json
    required_params = ["r1", "c1", "r2", "c2", "session_id"]
    for param in required_params:
        if param not in req_params:
            return Response(response="missing param", status=404)

    # make sure params are numeric
    numeric_params = ["r1", "c1", "r2", "c2"]
    for numeric_param in numeric_params:
        if not isinstance(req_params[numeric_param], int) and not req_params[numeric_param].isnumeric():
            return Response(response="not numeric", status=404)
    
    r1 = int(req_params["r1"])
    c1 = int(req_params["c1"])
    r2 = int(req_params["r2"])
    c2 = int(req_params["c2"])
    session_id = req_params['session_id']

    next_board = database.make_move(lock, session_id, (r1, c1, r2, c2))
    print(next_board)
    if next_board:
        return {"result": "success", "next_board": next_board}
    return {"result": "failure"}