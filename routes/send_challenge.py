from utils import database
from flask import (request, Response)

from app import bp, lock

@bp.route('/send-challenge', methods=(['POST']))
def send_challenge():
    # require session_id and name of player to send challenge to
    print(request.json)
    req_params = request.json
    required_params = ["session_id", "name"]
    for param in required_params:
        if param not in req_params:
            return Response(response="missing param", status=404)
    myName = database.get_name_for_session_id(lock, req_params['session_id'])
    print(myName)
    database.update_challenge(lock, myName, req_params['name'])
    return { "result" : "success" }