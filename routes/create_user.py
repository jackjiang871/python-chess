import datetime
import uuid
import json

from flask import (request, Response)

from utils import database
from app import bp

@bp.route('/create-user', methods=(['POST']))
def create_user():
    # give them a session token or something
    req_params = request.json
    required_params = ["name"]
    for param in required_params:
        if param not in req_params:
            return Response(response="missing param", status=404)
    name = req_params["name"]
    # store a session-id -> name pair
    session_id = str(uuid.uuid1())

    now = datetime.datetime.now()
    time_change = datetime.timedelta(minutes=5)
    new_time = now + time_change

    current_time_plus_five_minutes = new_time.strftime("%c")

    data = { 'users' : {}, 'session_ids' : {} }
    # get current users
    data = database.retrieve_and_delete_old_users()
    
    # add this user with new session id and ttl
    if name in data['users']:
        return {"result" : "name taken"}
    
    data['users'][name] = { "session_id" : session_id, "ttl" : current_time_plus_five_minutes }
    data['session_ids'][session_id] = {"name" : name, "ttl" : current_time_plus_five_minutes}

    with open('users.json', 'w') as outfile:
        json.dump(data, outfile)

    return {"result" : "name created", "session_id" : session_id}