import numpy as np

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

def get_move(player):
    print "Player %s:" % player
    x = input("What is the x-coordinate of your move? ")
    y = input("What is the y-coordinate of your move? ")
    return (x,y)

def make_move(boardarr, coords, player):
    if coords[0] > 2 or coords[1] > 2:
        raise Exception("That is outside of the board!")
    if boardarr[coords[1], coords[0]] != '_':
        raise Exception("There's already a marker there!")
    boardarr[coords[1], coords[0]] = player
    return boardarr

def check_win(boardarr):
    possiblewins = [list(boardarr[i]) for i in range(3)] + [list(boardarr.T[i]) for i in range(3)]
    possiblewins += [[boardarr[i,i] for i in range(3)]] + [[boardarr[i,2-i] for i in range(3)]]
    for possiblewin in possiblewins:
        if len(set(possiblewin)) == 1 and possiblewin[0] in ('X', 'O'):
            return possiblewin[0]
    return None

def check_draw(boardarr):
    if '_' not in boardarr and check_win(boardarr) is None:
        return True
    else:
        return False
  
    
board = new_board()
currentplayer = 'X'
move = None
winner = None
isDraw = False

while winner is None and not isDraw:
    while True:
        try:
            render(board)
            move = get_move(currentplayer)
            board = make_move(board, move, currentplayer)
            break
        except Exception:
            print "Try again."
    winner = check_win(board)
    move = None
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

