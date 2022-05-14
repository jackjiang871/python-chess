from flask import (
    Blueprint, render_template, request, Response
)
import chess
import json
import uuid
import os
import datetime

bp = Blueprint('chess_controller', __name__)

def retrieve_and_delete_old_users():
    should_rewrite = False
    data = { 'users' : {}, 'session_ids' : {} }

    # get current users
    if os.path.isfile('users.json'):
        with open('users.json') as json_file:
            data = json.load(json_file)
    else:
        return data
    users = data['users']
    users_to_delete = []
    session_ids_to_delete = []
    for name in users:
        now = datetime.datetime.now()
        ttl = datetime.datetime.strptime(users[name]['ttl'], '%c')
        if ttl < now:
            users_to_delete.append(name)
            session_ids_to_delete.append(users[name]['session_id'])
            should_rewrite = True
    for name in users_to_delete:
        del users[name]
    for session_id in session_ids_to_delete:
        del data['session_ids'][session_id]

    if should_rewrite:
        with open("users.json", 'w') as outfile:
            json.dump(data, outfile)

    return data

@bp.route('/update-board', methods=(['POST']))
def update_board():
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
    possible_moves = chess.get_possible_moves(next_board, 0 if turn else 1)

    return {"next_board": next_board, "possible_moves": possible_moves}

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
    data = retrieve_and_delete_old_users()
    
    # add this user with new session id and ttl
    if name in data['users']:
        return {"result" : "name taken"}
    
    data['users'][name] = { "session_id" : session_id, "ttl" : current_time_plus_five_minutes }
    data['session_ids'][session_id] = {"name" : name, "ttl" : current_time_plus_five_minutes}

    with open('users.json', 'w') as outfile:
        json.dump(data, outfile)

    return {"result" : "name created", "session_id" : session_id}

@bp.route('/get-players', methods=(['GET']))
def get_players():
    users_and_session_ids = retrieve_and_delete_old_users()
    print(users_and_session_ids)
    names = users_and_session_ids['users'].keys()
    return { "players" : list(names) }

@bp.route('/healthcheck', methods=(['GET']))
def healthcheck():
    # give them a session token or something
    return "ok"