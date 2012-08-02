"""
>>> is_complete([1,2,3,4,5,6,7,8,9])
True
>>> is_complete([1,5,5,5,5,2,3,4,1])
False
>>> is_complete([6,7,5,8,9,3,4,1,2])
True

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
"""
import pprint
# ok so there are two interesting things rules (and three ways the rules are applied)
# 1. <= one of each number
# 2. every number



def solve(board):
    is_complete = lambda nine_squares : all(i in nine_squares for i in range(9))
    is_legal = lambda nine_squares : all(len([s for s in nine_squares if s==i+1])<=1 for i in range(9))

    row = lambda b : [i for i in range(b*9,(b+1)*9)]
    col = lambda b : [i for i in range(b,81,9)]
    box = lambda b : [(b//3)*27+(b%3)*3+t*9+u for t in range(3) for u in range(3)]

    dex_gen = lambda section_func : (section_func(b) for b in range(9))
    sections = lambda board, dex_set_iter : ([board[index] for index in dex_set] for dex_set in dex_set_iter)
    find = lambda board, which, index : [nine_index for nine_index in sections(board, dex_gen(which)) if index in nine_index][0]

    make_move = lambda board, index, move : [board[i] if i == index else move for i in range(81)]
    legal_moves = lambda index : [i for i in range(1,10) if all(is_legal(find(make_move(board, index, i), sec, index) for sec in (row,col,box)))]
    
    empty_indicies = [i for i in range(81) if board[i] == 0]
    if not empty_indicies: return board #win
    
    print type( ( (i, legal_moves(i)) for i in empty_indicies))
    
    square_moves = (sort_tuple[1] for sort_tuple in sorted([(len(t[1]),t) for t in ( (i, legal_moves(i)) for i in empty_indicies)]))
    for index, moves in square_moves:
        for move in moves:
            solved = solve(make_move(board, index, move))
            if solved is not None: return solved
    return None
    
board = [0, 0, 3,  0, 2, 0,  6, 0, 0,
         9, 0, 0,  3, 0, 5,  0, 0, 1,
         0, 0, 1,  8, 0, 6,  4, 0, 0,
             
         0, 0, 8,  1, 0, 2,  9, 0, 0,
         7, 0, 0,  0, 0, 0,  0, 0, 8,
         0, 0, 6,  7, 0, 8,  2, 0, 0,
             
         0, 0, 2,  6, 0, 9,  5, 0, 0,
         8, 0, 0,  2, 0, 3,  0, 0, 9,
         0, 0, 5,  0, 1, 0,  3, 0, 0,]
'''
0 --> 0,1,2  9,10,11  18,19,20
1 --> 3,4,5  12,13,14 21,22,23
2 --> 6,7,8  15,16,17 24,25,26 

3 --> 27
4 --> 30
'''
'''
for r in range(3):
    for i in range(3):
        corner = r * 27 + i * 3
        
        box = [corner + t * 9 + u for t in range(3) for u in range(3)]
        
        print box
        
boxes = [ [(r*27+i*3)+t*9+u for t in range(3) for u in range(3)] for i in range(3) for r in range(3) ]
'''

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    
    '''
    for row in sections(board, dex_gen(row)):
        print row
    print '-'*27
    for col in sections(board, dex_gen(col)):
        print col
    print '-'*27
    for box in sections(board, dex_gen(box)):
        print box
    '''
        

    
    solved = solve(board)
