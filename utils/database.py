import datetime
import uuid
import copy

from flask import session
import chess
'''
'users': {
    name: {'sessionId': sessionId}
    ...
}
'session_ids': {
    session_id: {"name" : name, "game_id": game_id, "ttl" : ttl }
    ...
'games': {
    game_id: {"board": board, "white_session_id": session_id, "black_session_id": session_id, "currentMove": currentMove}
    ...
}
'challenges': {
    name: {
        'received': [],
        'sent': []
    }
    ...
}
'''
data = {'users': {}, 'session_ids' : {}, 'games': {}, 'challenges': {}}

# deletes all users that have exceeded their ttl
def delete_old_users(lock):
    users_to_delete = []
    session_ids_to_delete = []
    lock.acquire()
    for session_id in data['session_ids']:
        now = datetime.datetime.now()
        ttl = datetime.datetime.strptime(data['session_ids'][session_id]['ttl'], '%c')
        if ttl < now:
            users_to_delete.append(data['session_ids'][session_id]['name'])
            session_ids_to_delete.append(session_id)

    for name in users_to_delete:
        remove_all_challenges_for_name(name)
        del data['users'][name]
    for session_id in session_ids_to_delete:
        del data['session_ids'][session_id]
    lock.release()
    
def update_challenge(lock, sender_name, receiver_name):
    lock.acquire()
    if sender_name not in data['challenges']:
        data['challenges'][sender_name] = {'received': [], 'sent': []}
    if receiver_name not in data['challenges']:
        data['challenges'][receiver_name] = {'received': [], 'sent': []}
    data['challenges'][sender_name]['sent'].append(receiver_name)
    data['challenges'][receiver_name]['received'].append(sender_name)
    print(data)
    lock.release()

def remove_all_challenges_for_name(lock, name):
    lock.acquire()
    if name in data['challenges']:
        del data['challenges'][name]
    for n in data['challenges']:
        if name in data['challenges'][n]['sent']: data['challenges'][n]['sent'].remove(name)
        if name in data['challenges'][n]['received']: data['challenges'][n]['received'].remove(name)
    lock.release()

def remove_all_challenges_for_name(name):
    if name in data['challenges']:
        del data['challenges'][name]
    for n in data['challenges']:
        if name in data['challenges'][n]['sent']: data['challenges'][n]['sent'].remove(name)
        if name in data['challenges'][n]['received']: data['challenges'][n]['received'].remove(name)

def get_all_challenges(lock):
    delete_old_users(lock)
    lock.acquire()
    challenges = copy.deepcopy(data['challenges'])
    lock.release()
    return challenges

def get_all_usernames(lock):
    delete_old_users(lock)
    usernames = []
    lock.acquire()
    for username in data['users'].keys():
        usernames.append(username)
    lock.release()

    return usernames

def get_name_for_session_id(lock, session_id):
    lock.acquire()
    name = None
    if session_id in data['session_ids']:
        name = data['session_ids'][session_id]['name']
    lock.release()
    return name

def create_game(lock, white, black):
    lock.acquire()
    game_id = str(uuid.uuid1())
    data['games'][game_id] = {"board": copy.deepcopy(chess.board), 'white_session_id': white, 'black_session_id': black, 'currentMove': 0}
    lock.release()
    return game_id

def make_move(lock, session_id, move):
    lock.acquire()
    
    if session_id not in data['session_ids']:
        lock.release()
        return
    game_id = data['session_ids'][session_id]['game_id']
    if game_id == 0:
        lock.release()
        return
    
    if (session_id == data['games'][game_id]['white_session_id'] and data['games'][game_id]['currentMove'] == 0) or (session_id == data['games'][game_id]['black_session_id'] and data['games'][game_id]['currentMove'] == 1):
        r1, c1, r2, c2 = move
        currentMove = data['games'][game_id]['currentMove']
        data['games'][game_id]['board'] = chess.get_updated_board_if_is_valid_move(r1, c1, r2, c2, data['games'][game_id]['board'], currentMove)
        data['games'][game_id]['currentMove'] = (currentMove + 1) % 2
    lock.release()

def create_user(lock, name):
    delete_old_users(lock)
    # store a session-id -> name pair
    session_id = str(uuid.uuid1())

    now = datetime.datetime.now()
    time_change = datetime.timedelta(minutes=5)
    new_time = now + time_change

    current_time_plus_five_minutes = new_time.strftime("%c")

    lock.acquire()
    # add this user with new session id and ttl
    if name in data['users']:
        lock.release()
        return False
    
    data['users'][name] = { "session_id" : session_id }
    data['session_ids'][session_id] = {"name" : name, "game_id": 0, "ttl" : current_time_plus_five_minutes }

    lock.release()

    return session_id