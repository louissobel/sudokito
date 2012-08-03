"""
>>> is_legal([1,0,0,0,0,0,0,0,0,0])
True
>>> is_legal([1,0,0,0,1,0,0,0,0,0])
False
>>> is_legal([0,0,0,0,0,0,0,0,0,0])
True
>>> is_legal([1,0,0,0,2,0,5,0,0,0])
True
>>> is_legal([1,0,0,0,2,0,5,5,0,0])
False
>>> find(board, row, 12)
[9, 0, 0, 3, 0, 5, 0, 0, 1]
>>> legal_moves(board, 0)
[4, 5]

"""
row = lambda b : [i for i in range(b*9,(b+1)*9)]
col = lambda b : [i for i in range(b,81,9)]
box = lambda b : [(b//3)*27+(b%3)*3+t*9+u for t in range(3) for u in range(3)]
is_legal = lambda nine_squares : all(len([s for s in nine_squares if s==i+1])<=1 for i in range(9))
dex_gen = lambda section_func : (section_func(b) for b in range(9))
find = lambda board, which, index : [[board[i] for i in nine_index] for nine_index in dex_gen(which) if index in nine_index][0]
make_move = lambda board, index, move : [move if i == index else board[i] for i in range(81)]
legal_moves = lambda board, index : [i for i in range(1,10) if all([is_legal(find(make_move(board, index, i), sec, index)) for sec in (row,col,box)])]
square_moves = lambda board : (sort_tuple[1] for sort_tuple in sorted([(len(t[1]),t) for t in ( (i, legal_moves(board, i)) for i in range(81) if board[i] == 0)]))
def solve(board):
    if all(board): return board #win
    for index, move in reduce(lambda a,b : a + b, [[(index, move) for move in moves] for index, moves in square_moves(board)],[]):
        solved = solve(make_move(board, index, move))
        if solved is not None: return solved

    
board = [0, 0, 3,  0, 2, 0,  6, 0, 0,
         9, 0, 0,  3, 0, 5,  0, 0, 1,
         0, 0, 1,  8, 0, 6,  4, 0, 0,
             
         0, 0, 8,  1, 0, 2,  9, 0, 0,
         7, 0, 0,  0, 0, 0,  0, 0, 8,
         0, 0, 6,  7, 0, 8,  2, 0, 0,
             
         0, 0, 2,  6, 0, 9,  5, 0, 0,
         8, 0, 0,  2, 0, 3,  0, 0, 9,
         0, 0, 5,  0, 1, 0,  3, 0, 0,]


def is_complete(section):
    """
    checks that every section is 9 long and
    that every number appears
    """
    if not len(section) == 9:
        return False
    
    for i in range(1, 10):
        if not i in section:
            return False
    
    return True
    
def confirm(board):
    """
    Confirms that a board is a winner
    by checking every row, col, and box
    """
    for section_type in (row, col, box):
        section_indicies_gen = dex_gen(section_type)
        for section_indicies in section_indicies_gen:
            section = [board[i] for i in section_indicies]
            if not is_complete(section):
                print "Invalid:", section
                return False
    return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    solved = solve(board)
    if not confirm(solved):
        print "INVALID!!!!!"
    
    for row in [[solved[i] for i in d] for d in dex_gen(row)]:
        print row
        
