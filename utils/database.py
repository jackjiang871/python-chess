import datetime
import os
import json

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