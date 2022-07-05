from app import bp, lock
from flask import (request, Response)
import chess
import time
from utils import database

@bp.route('/next-board', methods=(['GET']))
def next_board():
    # get the game id for the session id
    req_params = request.args
    session_id = req_params.get('session_id')
    if session_id:
        game = database.get_game_for_session_id(lock, session_id)
        game['board']
        while True:
            if game['currentMove'] == database.data['games'][session_id]['currentMove']:
                pass # do something here