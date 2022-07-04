from utils import database
from app import bp, lock

@bp.route('/get-players', methods=(['GET']))
def get_players():
    players = database.get_all_usernames(lock)
    return { "players" : players }