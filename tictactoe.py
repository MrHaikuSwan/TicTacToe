import numpy as np
import sys
import random


def persist_rawinput(prompt, accepted_answers):
    answered = False
    while not answered:
        answer = raw_input(prompt).lower()
        if answer in accepted_answers:
            answered = True
        else:
            print "Try again."
    return answer
    
def new_board():
    boardarr = np.array([['_']*3]*3, dtype=str)
    return boardarr

def render(boardarr):
    row0 = list(boardarr[0])
    row1 = list(boardarr[1])
    row2 = list(boardarr[2])
    print "   0 1 2 X"
    print "  -------"
    print "0| %s %s %s |" % tuple(row0)
    print "1| %s %s %s |" % tuple(row1)
    print "2| %s %s %s |" % tuple(row2)
    print "Y -------"

def make_move(boardarr, coords, player):
    boardarr = boardarr.copy()
    if coords[0] > 2 or coords[1] > 2:
        raise Exception("That is outside of the board!")
    if boardarr[coords[1], coords[0]] != '_':
        raise Exception("There's already a marker there!")
    boardarr[coords[1], coords[0]] = player
    return boardarr

def check_win(boardarr):
    boardarr = boardarr.copy()
    possiblewins = [list(boardarr[i]) for i in range(3)] + [list(boardarr.T[i]) for i in range(3)]
    possiblewins += [[boardarr[i,i] for i in range(3)]] + [[boardarr[i,2-i] for i in range(3)]]
    for possiblewin in possiblewins:
        if len(set(possiblewin)) == 1 and possiblewin[0] in ('X', 'O'):
            return possiblewin[0]
    return None

def check_draw(boardarr):
    boardarr = boardarr.copy()
    if '_' not in boardarr and check_win(boardarr) is None:
        return True
    else:
        return False
    
def human_move(boardarr, player):
    boardarr = boardarr.copy()
    print "Player %s:" % player
    x = input("What is the x-coordinate of your move? ")
    y = input("What is the y-coordinate of your move? ")
    return (x,y)

#### Start AI's ####
def random_ai(boardarr, player):
    boardarr = boardarr.copy()
    available_moves = [(x,y) for y in range(len(boardarr)) for x in range(len(boardarr[y])) if boardarr [y,x] == '_']
    return random.choice(available_moves)

def winmove_ai(boardarr, player):
    boardarr = boardarr.copy()
    available_moves = [(x,y) for y in range(len(boardarr)) for x in range(len(boardarr[y])) if boardarr [y,x] == '_']
    possiblewins = [[(boardarr[i,j], (j,i)) for j in range(len(boardarr[i]))] for i in range(3)]
    possiblewins += [[(boardarr.T[i,j], (i,j)) for j in range(len(boardarr.T[i]))] for i in range(3)]
    possiblewins += [[(boardarr[i,i], (i,i)) for i in range(3)]] + [[(boardarr[i,2-i], (2-i,i)) for i in range(3)]]
    winning_moves = []
    for possiblewin in possiblewins:
        possiblewin.sort()
        onlymarkerposwin = [i[0] for i in possiblewin]
        if onlymarkerposwin == [player, player, '_']:
            winmove = possiblewin[2][1]
            winning_moves.append(winmove)
    if winning_moves != []:
        return random.choice(winning_moves)
    else:
        return random.choice(available_moves)

def winmove_blockloss_ai(boardarr, player):
    boardarr = boardarr.copy()
    if player == 'X':
        other_player = 'O'
    else:
        other_player = 'X'
    available_moves = [(x,y) for y in range(len(boardarr)) for x in range(len(boardarr[y])) if boardarr [y,x] == '_']
    possiblewins = [[(boardarr[i,j], (j,i)) for j in range(len(boardarr[i]))] for i in range(3)]
    possiblewins += [[(boardarr.T[i,j], (i,j)) for j in range(len(boardarr.T[i]))] for i in range(3)]
    possiblewins += [[(boardarr[i,i], (i,i)) for i in range(3)]] + [[(boardarr[i,2-i], (2-i,i)) for i in range(3)]]
    winning_moves = []
    blocking_moves = []
    for possiblewin in possiblewins:
        possiblewin.sort()
        onlymarkerposwin = [i[0] for i in possiblewin]
        if onlymarkerposwin == [player, player, '_']:
            winmove = possiblewin[2][1]
            winning_moves.append(winmove)
        if onlymarkerposwin == [other_player, other_player, '_']:
            blockmove = possiblewin[2][1]
            blocking_moves.append(blockmove)
    if winning_moves != []:
        return random.choice(winning_moves)
    elif blocking_moves != []:
        return random.choice(blocking_moves)
    else:
        return random.choice(available_moves)


def minimax_score(boardarr, player):
    boardarr = boardarr.copy()
    if check_win(boardarr) == 'X':
        return 10
    elif check_win(boardarr) == 'O':
        return -10
    elif check_draw(boardarr):
        return 0
    
    if player == 'X':
        other_player = 'O'
    else:
        other_player = 'X'
    available_moves = [(x,y) for y in range(len(boardarr)) for x in range(len(boardarr[y])) if boardarr [y,x] == '_']
    scores = []
    for move in available_moves:
        new_board = make_move(boardarr, move, player)
        score = minimax_score(new_board, other_player)
        scores.append(score)
    if player == 'X':
        return max(scores)
    else:
        return min(scores)
    
def minimax_ai(boardarr, player):
    boardarr = boardarr.copy()
    if player == 'X':
        other_player = 'O'
    else:
        other_player = 'X'
    available_moves = [(x,y) for y in range(len(boardarr)) for x in range(len(boardarr[y])) if boardarr [y,x] == '_']
    move_scores = {}
    scorevalues = []
    for move in available_moves:
        new_board = make_move(boardarr, move, player)
        score = minimax_score(new_board, other_player)
        move_scores[move] = score
        scorevalues.append(score)
    if player == 'X':
        best_score = max(scorevalues)
    else:
        best_score = min(scorevalues)
    move = next(key for key, value in move_scores.iteritems() if value == best_score)
    return move
        
#### End AI's ####
        
ailookup = {
        "random_ai": random_ai,
        "winmove_ai": winmove_ai,
        "winmove_blockloss_ai": winmove_blockloss_ai,
        "minimax_ai": minimax_ai}

AI = []
args = [i.lower() for i in sys.argv[1:3]]
if args[0] in ailookup:
    AI.append('X')
    def x_ai_move(boardarr, player):
        func = ailookup[args[0]]
        return func(boardarr, player)
    
if args[1] in ailookup:
    AI.append('O')
    def o_ai_move(boardarr, player):
        func = ailookup[args[1]]
        return func(boardarr, player)
    
board = new_board()
currentplayer = 'X'
winner = None
isDraw = False

while winner is None and not isDraw:
    while True:
        render(board)
        if currentplayer in AI:
            if currentplayer == 'X':
                move = x_ai_move(board, currentplayer)
            elif currentplayer == 'O':
                move = o_ai_move(board, currentplayer)
            board = make_move(board, move, currentplayer)
            break
        else:
            try:
                move = human_move(board, currentplayer)
                board = make_move(board, move, currentplayer)
                break
            except Exception:
                print "Try again.\n"
                
    winner = check_win(board)
    if winner is None:
        isDraw = check_draw(board)
    if currentplayer == 'X':
        currentplayer = 'O'
    else:
        currentplayer = 'X'

render(board)
if isDraw:
    print "It's a draw!"
else:
    print "Player %s won!" % winner
