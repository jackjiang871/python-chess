from utils import database
from app import bp, lock
from flask import (request, Response)


@bp.route('/get-players', methods=(['GET']))
def get_players():
    req_params = request.args
    session_id = req_params.get('session_id')
    print(session_id)
    challengers = []
    challenged = []
    if session_id:
        name = database.get_name_for_session_id(lock, session_id)
        challenges = database.get_all_challenges(lock)
        print(challenges)
        if name in challenges:
            print(challenges[name])
            challengers = challenges[name]['received']
            challenged = challenges[name]['sent']
    
    players = database.get_all_usernames(lock)
    return { "players" : players, "challengers" : challengers, "challenged": challenged }