from utils import database

from app import bp
@bp.route('/get-players', methods=(['GET']))
def get_players():
    users_and_session_ids = database.retrieve_and_delete_old_users()
    print(users_and_session_ids)
    names = users_and_session_ids['users'].keys()
    return { "players" : list(names) }