from flask import (request, Response)

from utils import database
from app import bp, lock

@bp.route('/create-user', methods=(['POST']))
def create_user():
    # give them a session token or something
    req_params = request.json
    required_params = ["name"]
    for param in required_params:
        if param not in req_params:
            return Response(response="missing param", status=404)
    name = req_params["name"]
    session_id = database.create_user(lock, name)

    return {"result" : "name created", "session_id" : session_id} if session_id else {"result" : "name taken"}