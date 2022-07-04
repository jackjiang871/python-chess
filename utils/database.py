import datetime
import uuid

data = {'users': {}, 'session_ids' : {}, 'games': {}}

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
        del data['users'][name]
    for session_id in session_ids_to_delete:
        del data['session_ids'][session_id]
    lock.release()

def get_all_usernames(lock):
    delete_old_users(lock)
    usernames = []
    lock.acquire()
    for username in data['users'].keys():
        usernames.append(username)
    lock.release()

    return usernames

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
    data['session_ids'][session_id] = {"name" : name, "ttl" : current_time_plus_five_minutes }

    lock.release()

    return session_id