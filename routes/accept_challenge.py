from utils import database
from flask import (request, Response)

from app import bp, lock

@bp.route('/accept-challenge', methods=(['POST']))
def accept_challenge():
    # require session_id and name of player to send challenge to
    print(request.json)
    req_params = request.json
    required_params = ["session_id", "name"]
    for param in required_params:
        if param not in req_params:
            return Response(response="missing param", status=404)
        
    challenges = database.get_all_challenges(lock)
    myName = database.get_name_for_session_id(lock, req_params['session_id'])
    yourName = req_params['name']
    print(challenges)
    if yourName in challenges[myName]['received']:
        database.remove_all_challenges_for_name(yourName)
        database.remove_all_challenges_for_name(myName)
    else:
        return { "result" : "failure" }
    print(database.get_all_challenges(lock))
    return { "result" : 'success' }