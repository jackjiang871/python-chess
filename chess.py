from copy import copy
import math
from unicodedata import name
'''

'''
board = [['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
         ['♟' for _ in range(8)],
         [' ' for _ in range(8)],
         [' ' for _ in range(8)],
         [' ' for _ in range(8)],
         [' ' for _ in range(8)],
         ['♙' for _ in range(8)],
         ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']]
black_pieces = ['♟', '♜', '♞', '♝', '♛', '♚', '♟e', '♚m', '♜m']
white_pieces = ['♙', '♖', '♘', '♗', '♕', '♔', '♙e', '♔m', '♖m']

def get_new_board():
    return board

def get_black_pieces():
    return black_pieces

def get_white_pieces():
    return white_pieces

# turn - 0: white 1: black
def get_updated_board_if_is_valid_move(r1, c1, r2, c2, board, turn):
    if turn == 0 and board[r1][c1] in black_pieces:
        print("invalid move: white's move")
        return board
    elif turn == 1 and board[r1][c1] in white_pieces:
        print("invalid move: black's move")
        return board
    next_board = get_updated_board_if_is_valid_move_without_king_check(r1, c1, r2, c2, board)
    if next_board:
        r, c = 0, 0
        if board[r1][c1] in white_pieces:
            for i in range(8):
                for j in range(8):
                    piece = board[i][j]
                    if piece in ['♔', '♔m']:
                        r, c = i, j
        elif board[r1][c1] in black_pieces:
            for i in range(8):
                for j in range(8):
                    piece = board[i][j]
                    if piece in ['♚', '♚m']:
                        r, c = i, j
        if can_be_captured(r, c, next_board):
            print("will be put in check")
            return board
        else:
            turn = 0 if turn else 1
            return next_board
    else:
        print("invalid move")
        return board

def get_updated_board_if_is_valid_move_without_king_check(r1, c1, r2, c2, board):
    coordinates_are_outside_board = r1 < 0 or c1 < 0 or r2 < 0 or c2 < 0 or r1 > 7 or c1 > 7 or r2 > 7 or c2 > 7
    if coordinates_are_outside_board or (r1, c1) == (r2, c2):
        return None
    piece = board[r1][c1]
    move_to = board[r2][c2]

    if piece == ' ':
        return None

    same_team_piece_on_move_to_square = (piece in black_pieces and move_to in black_pieces) or (piece in white_pieces and move_to in white_pieces)
    if same_team_piece_on_move_to_square:
        return None

    # Copy board
    next_board = remove_en_passant([row[:] for row in board])

    if piece in ['♙','♟','♙e','♟e']:
        if piece == '♙' or piece == '♙e':
            move_dir = -1
            move_two = r2 - r1 == move_dir * 2 and r1 == 6 and board[r1 + move_dir][c1] == ' ' and move_to == ' ' and c1 == c2
            move_one = r2 - r1 == move_dir and move_to == ' ' and c1 == c2
            capture_left = r2 - r1 == move_dir and c2 - c1 == -1 and move_to in black_pieces
            capture_right = r2 - r1 == move_dir and c2 - c1 == 1 and move_to in black_pieces
            en_passant_left = r2 - r1 == move_dir and c2 - c1 == -1 and move_to == ' ' and board[r1][c2] == '♟e'
            en_passant_right = r2 - r1 == move_dir and c2 - c1 == 1 and move_to == ' ' and board[r1][c2] == '♟e'
            if move_two:
                next_board[r1][c1] = ' '
                next_board[r2][c2] = '♙e'
                return next_board
            elif move_one or capture_left or capture_right:
                next_board[r1][c1] = ' '
                if r2 == 0:
                    next_board[r2][c2] = '♕'
                else:
                    next_board[r2][c2] = '♙'
                return next_board
            elif en_passant_left or en_passant_right:
                next_board[r1][c1] = ' '
                next_board[r1][c2] = ' '
                next_board[r2][c2] = '♙'
                return next_board
            else:
                return None
            
        if piece == '♟' or piece == '♟e':
            move_dir = 1
            move_two = r2 - r1 == move_dir * 2 and r1 == 1 and board[r1 + move_dir][c1] == ' ' and move_to == ' ' and c1 == c2
            move_one = r2 - r1 == move_dir and move_to == ' ' and c1 == c2
            capture_left = r2 - r1 == move_dir and c2 - c1 == -1 and move_to in white_pieces
            capture_right = r2 - r1 == move_dir and c2 - c1 == 1 and move_to in white_pieces
            en_passant_left = r2 - r1 == move_dir and c2 - c1 == -1 and move_to == ' ' and board[r1][c2] == '♙e'
            en_passant_right = r2 - r1 == move_dir and c2 - c1 == 1 and move_to == ' ' and board[r1][c2] == '♙e'
            if move_two:
                next_board[r1][c1] = ' '
                next_board[r2][c2] = '♟e'
                return next_board
            elif move_one or capture_left or capture_right:
                next_board[r1][c1] = ' '
                if r2 == 7:
                    next_board[r2][c2] = '♛'
                else:
                    next_board[r2][c2] = '♟'
                return next_board
            elif en_passant_left or en_passant_right:
                next_board[r1][c1] = ' '
                next_board[r1][c2] = ' '
                next_board[r2][c2] = '♟'
                return next_board
            else:
                return None
    if piece in ['♚','♔','♚m','♔m']:
        # castle right
        if (piece == '♚' and (r2, c2) == (r1, 6) and board[r1][7] == '♜' 
            and board[r1][6] == ' ' and board[r1][5] == ' ' and not can_be_captured(r1, c1, board)):
            board[r1][5] = '♞'
            board[r1][6] = '♞'
            for i in range(8):
                for j in range(8):
                    if (board[i][j] in white_pieces and
                        (get_updated_board_if_is_valid_move_without_king_check(i,j,r1,6,board) or 
                        get_updated_board_if_is_valid_move_without_king_check(i,j,r1,5,board))):
                        return None
            board[r1][5] = ' '
            board[r1][6] = ' '
            next_board[r1][4] = ' '
            next_board[r1][5] = '♜m'
            next_board[r1][6] = '♚m'
            next_board[r1][7] = ' '
            return next_board
        if (piece == '♔' and (r2, c2) == (r1, 6) and board[r1][7] == '♖' 
            and board[r1][6] == ' ' and board[r1][5] == ' ' and not can_be_captured(r1, c1, board)):
            board[r1][5] = '♘'
            board[r1][6] = '♘'
            for i in range(8):
                for j in range(8):
                    if (board[i][j] in black_pieces and
                        (get_updated_board_if_is_valid_move_without_king_check(i,j,r1,6,board) or 
                        get_updated_board_if_is_valid_move_without_king_check(i,j,r1,5,board))):
                        return None
            board[r1][5] = ' '
            board[r1][6] = ' '
            next_board[r1][4] = ' '
            next_board[r1][5] = '♖m'
            next_board[r1][6] = '♔m'
            next_board[r1][7] = ' '
            return next_board

        # castle left
        if (piece == '♚' and (r2, c2) == (r1, 2) and board[r1][0] == '♜'
            and board[r1][1] == ' ' and board[r1][2] == ' ' and board[r1][3] == ' ' and not can_be_captured(r1, c1, board)):
            board[r1][2] = '♞'
            board[r1][3] = '♞'
            for i in range(8):
                for j in range(8):
                    if (board[i][j] in white_pieces and
                        (get_updated_board_if_is_valid_move_without_king_check(i,j,r1,2,board) or
                        get_updated_board_if_is_valid_move_without_king_check(i,j,r1,3,board))):
                        return None
            board[r1][2] = ' '
            board[r1][3] = ' '
            next_board[r1][4] = ' '
            next_board[r1][3] = '♜m'
            next_board[r1][2] = '♚m'
            next_board[r1][0] = ' '
            return next_board
        if (piece == '♔' and (r2, c2) == (r1, 2) and board[r1][0] == '♖'
            and board[r1][1] == ' ' and board[r1][2] == ' ' and board[r1][3] == ' ' and not can_be_captured(r1, c1, board)): 
            board[r1][2] = '♘'
            board[r1][3] = '♘'
            for i in range(8):
                for j in range(8):
                    if (board[i][j] in black_pieces and
                        (get_updated_board_if_is_valid_move_without_king_check(i,j,r1,2,board) or
                        get_updated_board_if_is_valid_move_without_king_check(i,j,r1,3,board))):
                        return None
            board[r1][2] = ' '
            board[r1][3] = ' '
            next_board[r1][4] = ' '
            next_board[r1][3] = '♖m'
            next_board[r1][2] = '♔m'
            next_board[r1][0] = ' '
            return next_board
        # regular king move
        if abs(r2 - r1) < 2 and abs(c2 - c1) < 2:
            if len(piece) == 1:
                next_board[r2][c2] = piece + 'm'
            else:
                next_board[r2][c2] = piece
            next_board[r1][c1] = ' '
            return next_board
    if piece in ['♜m', '♜', '♖m', '♖']:
        # make sure no piece in between r1,c1 and r2,c2
        if r1 - r2 == 0:
            r = range(c1+1, c2) if c1 < c2 else range(c2 + 1, c1)
            for i in r:
                if board[r1][i] != ' ':
                    return None
            next_board[r1][c1] = ' '
            if len(piece) == 1:
                next_board[r2][c2] = piece + 'm'
            else:
                next_board[r2][c2] = piece
            return next_board
        elif c1 - c2 == 0:
            r = range(r1+1, r2) if r1 < r2 else range(r2 + 1, r1)
            for i in r:
                if board[i][c1] != ' ':
                    return None
            next_board[r1][c1] = ' '
            if len(piece) == 1:
                next_board[r2][c2] = piece + 'm'
            else:
                next_board[r2][c2] = piece
            return next_board
    if piece in ['♞', '♘']:
        if (abs(r2 - r1) == 1 and abs(c2 - c1) == 2) or (abs(r2 - r1) == 2 and abs(c2 - c1) == 1):
            next_board[r1][c1] = ' '
            next_board[r2][c2] = piece
            return next_board
    if piece in ['♝', '♗']:
        if (c2 - c1) ==  0:
            return None
        if abs((r2 - r1) // (c2 - c1)) == 1 and (r2 - r1) % (c2 - c1) == 0:
            for i in range(1,abs(r2-r1)):
                if r2 > r1 and c2 > c1 and board[r1+i][c1+i] != ' ':
                    return None
                if r2 < r1 and c2 < c1 and board[r1-i][c1-i] != ' ':
                    return None
                if r2 > r1 and c2 < c1 and board[r1+i][c1-i] != ' ':
                    return None
                if r2 < r1 and c2 > c1 and board[r1-i][c1+i] != ' ':
                    return None
            next_board[r1][c1] = ' '
            next_board[r2][c2] = piece
            return next_board
    if piece in ['♛', '♕']:
        if r1 - r2 == 0:
            r = range(c1+1, c2) if c1 < c2 else range(c2 + 1, c1)
            for i in r:
                if board[r1][i] != ' ':
                    return None
            next_board[r1][c1] = ' '
            next_board[r2][c2] = piece
            return next_board
        elif c1 - c2 == 0:
            r = range(r1+1, r2) if r1 < r2 else range(r2 + 1, r1)
            for i in r:
                if board[i][c1] != ' ':
                    return None
            next_board[r1][c1] = ' '
            next_board[r2][c2] = piece
            return next_board
            #13 04
        elif abs((r2 - r1) // (c2 - c1)) == 1 and (r2 - r1) % (c2 - c1) == 0:
            for i in range(1,abs(r2-r1)):
                if r2 > r1 and c2 > c1 and board[r1+i][c1+i] != ' ':
                    return None
                if r2 < r1 and c2 < c1 and board[r1-i][c1-i] != ' ':
                    return None
                if r2 > r1 and c2 < c1 and board[r1+i][c1-i] != ' ':
                    return None
                if r2 < r1 and c2 > c1 and board[r1-i][c1+i] != ' ':
                    return None
            next_board[r1][c1] = ' '
            next_board[r2][c2] = piece
            return next_board

def remove_en_passant(board):
    new_board = []
    for i in range(8):
        for j in range(8):
            piece_to_insert = board[i][j]
            if len(board[i][j]) == 2 and board[i][j][1] == 'e':
                piece_to_insert = board[i][j][0]
            if j == 0:
                new_board.append([piece_to_insert])
            else:
                new_board[i].append(piece_to_insert)
    return new_board

def can_be_captured(r1, c1, board):
    for i in range(8):
        for j in range(8):
            if get_updated_board_if_is_valid_move_without_king_check(i,j,r1,c1, board):
                print("captured: ", i, j, r1, c1)
                return True
    
    return False

def print_board(board):
    if board:
        print ("  0 1 2 3 4 5 6 7")
        i = 0
        for row in board:
            print (i, end=" ")
            for piece in row:
                if len(piece) == 2:
                    print(piece, end='')
                else:
                    print(piece, end=' ')
            print('')
            i += 1
        print(" ")
    else:
        print("nope")

def compare_board(b1, b2):
    assert(len(b1) == 8)
    assert(len(b2) == 8)
    for i in range(len(b1)):
        assert(len(b1[i]) == 8)
        assert(len(b2[i]) == 8)
        for j in range(len(b1[i])):
            if b1[i][j] != b2[i][j]:
                return False
    return True

def start_game():

    board = [['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
            ['♟' for _ in range(8)],
            [' ' for _ in range(8)],
            [' ' for _ in range(8)],
            [' ' for _ in range(8)],
            [' ' for _ in range(8)],
            ['♙' for _ in range(8)],
            ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']]
    turn = 0
    while True:
        print_board(board)
        print("r1","c1","r2","c2")
        
        user_input = str(input()).replace(" ", "")[:4]
        if user_input == 'quit':
            break
        prevboard = board.copy()
        board = get_updated_board_if_is_valid_move(int(user_input[0]),int(user_input[1]),int(user_input[2]),int(user_input[3]), board, turn)
        if not compare_board(board, prevboard):
            turn = 0 if turn else 1

if __name__ == "__main__":
    start_game()