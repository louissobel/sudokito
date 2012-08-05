"""
A functional soduku solver algorithm written in 10 lines of python
Also, a 174 line expanded version
"""

def small_solver(board):
    """
    namespace the small solver    
    """
    # The solver
    # ----------------------------------------------------------------------------------------------
    rows = lambda s : [i for i in range(s*9, (s+1)*9)]
    cols = lambda s : [i for i in range(s, 81, 9)]
    boxs = lambda s : [(s//3)*27+(s%3)*3 + (i//3)*9+(i%3) for i in range(9)]
    is_legal = lambda ns, v : True if v==10 else False if len([s for s in ns if s==v]) > 1 else is_legal(ns, v+1)
    find = lambda b, sg, i, ni : [b[j] for j in ni] if i in ni else find(b, sg, i, sg.next())
    make_move = lambda b, i, m : [m if j == i else b[j] for j in range(81)]
    legal_moves = lambda b, i : [m for m in range(1, 10) if all([is_legal(find(make_move(b, i, m), (s(si) for si in range(9)), i, []), 1) for s in (rows, cols, boxs)])]
    square_moves = lambda b : min(((i, legal_moves(b, i)) for i in range(81) if not b[i]),key=lambda x : len(x[1]))
    solve_helper = lambda g, l, t : l if l else None if t == 0 else solve_helper(g, g.next(), t - 1)
    solve = lambda b : b if all(b) else (lambda i, ms : None if not ms else solve_helper((solve(make_move(b, i, m)) for i, m in [(i, m) for m in ms]), None, len(ms)))(*square_moves(b))
    # ----------------------------------------------------------------------------------------------
    return solve(board)

def unrolled(board):
    """
    namespace the expanded functions
    
    """
    # The solver
    # ----------------------------------------------------------------------------------------------
    def rows(section_index):
        """
        Returns the nine indicies of the bth row
        """
        out = []
        start = section_index * 9
        end = (section_index + 1) * 9
        for i in range(start, end):
            out.append(i)
        return out
        
    def cols(section_index):
        """
        Returns the nine indicies of the bth column
        """
        out = []
        for i in range(section_index, 81, 9):
            out.append(i)
        return out
        
    def boxs(section_index):
        """
        Returns the nine indicies of the bth box
        """
        out = []
        for s in range(9):
            corner = (section_index // 3) * 27 + (section_index % 3 ) * 3
            i = corner + (s // 3) * 9 + (s % 3)
            out.append(i)
        return out
        
    def is_legal(nine_squares, value):
        """
        Checks if the nine_squares are in a legal
        state using a recursive search on value.
        
        Value is the number to check that it appears
        once or zero times. If this function is called 
        initially with value 1, will check all values.
        """
        if value == 10:
            return True
        
        count = 0
        for square in nine_squares:
            if square == value:
                count += 1
        if count > 1:
            return False
            
        return is_legal(nine_squares, value + 1)
        
        
    def find(board, section_generator, index, nine_indicies):
        """
        Gets the values of the section whose generating function
        is specified by which and contains the index index
        
        Recursively searches for it using the generator
        (this is so the search only descends as deep as necessary)
        """
        if index in nine_indicies:
            out = []
            for i in nine_indicies:
                out.append(board[i])
            return out
        
        return find(board, section_generator, index, section_generator.next())
        
    def make_move(board, index, move):
        """
        Returns a new board, but with the number
        move inserted at the given index
        """
        new_board = []
        for i in range(81):
            if i == index:
                value = move
            else:
                value = board[i]
            new_board.append(value)
        return new_board
        
    def legal_moves(board, index):
        """
        Given a board and an index, will return the list
        of all legal moves at that index
        """
        def section_generator(section):
            for i in range(9):
                yield section(i)        
        
        out = []
        for move in range(1, 10):
            legal = True
            new_board = make_move(board, index, move)
            for section in (rows, cols, boxs):
                new_section = find(new_board, section_generator(section), index, [])
                new_section_is_legal = is_legal(new_section, 1)
                legal = legal * new_section_is_legal
            
            if legal:
                out.append(move)
        return out
    
    def square_moves(board):
        """
        Given a board, returns the empty index with
        the least amount of legal moves and the list
        of those moves as a tuple.
        
        The first value is the index, the second value
        is the list of legal moves for that index.
        """
        legal_list = []
        for i in range(81):
            if board[i] == 0:
                legal_move_list = legal_moves(board, i)
                index_move_list = (i, legal_move_list)
                legal_list.append(index_move_list)
        
        # and now find the one with the smallest list length
        best = None
        for index_move_list in legal_list:
            if best is None:
                best = index_move_list
            else:
                index, move_list = index_move_list
                best_index, best_move_list = best
                if len(move_list) < len(best_move_list):
                    best = index_move_list
        
        return best
        
    def solve_helper(gen, last, tries, max):
        """
        Used by solve to return when we find something that works
        (so as not to try the remaining, incorrect, legal_moves)
        
        this replaces code in solve that may have looked like this:
        
        ```
        for solution in solver_gen:
           if solution is not None:
               return solution
        ```
        
        But doing it this way allows it to be inlined in the compressed solver
        """
        if last is not None:
            return last
        
        if tries == max: # this avoids a StopIteration ever being raised
            return None
            
        return solve_helper(gen, gen.next(), tries + 1, max)
        
    
    def solve(board):
        """
        Recursively solves a sudoku by creating a generator that will
        repeatedly try different legal moves by recursively calling solve,
        and passing it to solve_helper
        
        Returns the board passed in if every space is filled. That is a win
        condition, as the algorithm only makes a move if there it is legal move.
        
        An assumption is that the board passed in must be in a legal state.
        """
        empty_count = 0
        for v in board:
            if v == 0:
                empty_count += 1
        if empty_count == 0:
            # win.
            return board

        index, moves = square_moves(board)
        if not moves:
            return None
        
        def solver_gen():
            for move in moves:
                new_board = make_move(board, index, move)
                yield solve(new_board)
            
        # Call solve_helper with the initial values
        return solve_helper(solver_gen(), None, 0, len(moves))
    # ----------------------------------------------------------------------------------------------
    return solve(board)

# -------------------
# Testing functions
def print_board(board):
    for i in range(81):
        print board[i],
        if  i % 9 == 8:
            print
            
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
    
    # I have to copy these to here
    row = lambda b : [i for i in range(b*9,(b+1)*9)]
    col = lambda b : [i for i in range(b,81,9)]
    box = lambda b : [(b//3)*27+(b%3)*3+t*9+u for t in range(3) for u in range(3)]
    dex_gen = lambda section_func : (section_func(b) for b in range(9))
    
    for section_type in (row, col, box):
        section_indicies_gen = dex_gen(section_type)
        for section_indicies in section_indicies_gen:
            section = [board[i] for i in section_indicies]
            if not is_complete(section):
                return False
    return True  
    
def test(board_dict, solver_dict):
    """
    Tests the given boards with
    the given solvers
    """
    import time
    print "Testing %d sudoku solvers with %d boards" % (len(solver_dict), len(board_dict))
    failures = False
    for name, board in board_dict.items():
        print '-' * 50
        print 'Board "%s":' % name
        
        for solver_name, solver in solver_dict.items():
            print "Solver %s......" % solver_name,
            start = time.time()
            solution = solver(board)
            end = time.time()
            
            if solution is None:
                print ".. NO SOLUTION FOUND [%fs]" % (end - start)
            elif confirm(solution):
                print ".. OK [%fs]" % (end - start)
            else:
                print ".. !!!! FAILED"
                failures = True
                
    if failures:
        print "!!!! There was a failure."
        
# ------------------
# Testing data

hn_board = [
    0, 0, 3,  0, 2, 0,  6, 0, 0,
    9, 0, 0,  3, 0, 5,  0, 0, 1,
    0, 0, 1,  8, 0, 6,  4, 0, 0,

    0, 0, 8,  1, 0, 2,  9, 0, 0,
    7, 0, 0,  0, 0, 0,  0, 0, 8,
    0, 0, 6,  7, 0, 8,  2, 0, 0,

    0, 0, 2,  6, 0, 9,  5, 0, 0,
    8, 0, 0,  2, 0, 3,  0, 0, 9,
    0, 0, 5,  0, 1, 0,  3, 0, 0,
]

hard_board = [
    9, 0, 0,  0, 0, 3,  0, 0, 7,
    8, 0, 0,  0, 0, 0,  0, 0, 1,
    0, 0, 3,  2, 0, 0,  8, 6, 4,

    0, 6, 0,  0, 2, 7,  0, 0, 0,
    0, 8, 1,  0, 0, 4,  0, 0, 0,
    0, 0, 0,  0, 3, 0,  0, 0, 0,

    0, 0, 0,  0, 0, 9,  3, 5, 2,
    0, 0, 0,  0, 0, 5,  0, 0, 0,
    1, 0, 0,  0, 0, 0,  4, 7, 0,
]

evil_005 = [
    8, 0, 6,  0, 2, 0,  0, 0, 0,
    7, 4, 0,  0, 0, 3,  0, 0, 8,
    0, 0, 0,  0, 5, 0,  0, 3, 0,
                              
    5, 0, 0,  4, 0, 0,  8, 0, 0,
    6, 0, 0,  0, 0, 0,  0, 0, 7,
    0, 0, 7,  0, 0, 2,  0, 0, 1,
                              
    0, 7, 0,  0, 6, 0,  0, 0, 0,
    4, 0, 0,  8, 0, 0,  0, 1, 6,
    0, 0, 0,  0, 4, 0,  9, 0, 2,
]

TEST_BOARDS = {
    'hn_board' : hn_board,
    'hard_board' : hard_board,
    '6.005 evil' : evil_005,
}

SOLVER_DICT = {
    'small' : small_solver,
    'unrolled' : unrolled,
}



if __name__ == "__main__":
    
    test(TEST_BOARDS, SOLVER_DICT)