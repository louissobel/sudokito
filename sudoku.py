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
# ----------------------------------------------------------------------------------------------
row = lambda b : [i for i in range(b*9,(b+1)*9)]
col = lambda b : [i for i in range(b,81,9)]
box = lambda b : [(b//3)*27+(b%3)*3+t*9+u for t in range(3) for u in range(3)]
is_legal = lambda nine_squares : all(len([s for s in nine_squares if s==v])<=1 for v in range(1, 10))
dex_gen = lambda section_func : (section_func(b) for b in range(9))
find = lambda board, which, index : [[board[i] for i in nine_index] for nine_index in dex_gen(which) if index in nine_index][0]
make_move = lambda board, index, move : [move if i == index else board[i] for i in range(81)]
legal_moves = lambda board, index : [v for v in range(1,10) if all([is_legal(find(make_move(board, index, v), sec, index)) for sec in (row,col,box)])]
square_moves = lambda board : (sort_tuple[1] for sort_tuple in sorted([(len(t[1]),t) for t in ( (i, legal_moves(board, i)) for i in range(81) if board[i] == 0)]))
def solve(board):
    if all(board): return board #win
    for index, move in reduce(lambda a,b : a + b, [[(index, move) for move in moves] for index, moves in square_moves(board)],[]):
        solved = solve(make_move(board, index, move))
        if solved is not None: return solved
# ----------------------------------------------------------------------------------------------
    
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

def unrolled():
    """
    namespace the expanded functions
    """
    def row(b):
        """
        Returns the nine indicies of the bth row
        """
        out = []
        start = b * 9
        end = (b + 1) * 9
        for i in range(start, end):
            out.append(i)
        return out
        
    def col(b):
        """
        Returns the nine indicies of the bth column
        """
        out = []
        for i in range(b, 81, 9):
            out.append(i)
        return out
        
    def box(b):
        """
        Returns the nine indicies of the bth box
        """
        out = []
        for col in range(3):
            for row in range(3):
                corner = (b // 3) * 27 + (b % 3 ) * 3
                i = corner + row * 9 + col
                out.append(i)
        return out
        
    def is_legal(nine_squares):
        """
        Checks if the nine given squares are in a legal state:
        each number appears once or zero times
        """
        for v in range(1, 10):
            count = 0
            for square in nine_squares:
                if square == v:
                    count += 1
            if not count <= 1:
                return False
        return True
        
    def dex_gen(section_func):
        """
        Given a function that takes an index and returns
        a set of nine indicies, (like row, col, and box)
        will return a generator that returns the value of
        that function for each index in 0 - 9
        """
        index = 0
        while True:
            if index == 9:
                raise StopIteration
            yield section_func(index)
            index += 1
        
    def find(board, which, index):
        """
        Gets the values of the section whose generating function
        is specified by which and contains the index index
        """
        section_indicies_gen = dex_gen(which)
        for section_indicies in section_indicies_gen:
            if index in section_indicies:
                out = []
                for i in section_indicies:
                    out.append(board[i])
                return out
        
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
        out = []
        for v in range(1, 10):
            legal = True
            new_board = make_move(board, index, v)
            for section_type in (row, col, box):
                new_section = find(new_board, section_type, index)
                new_section_is_legal = is_legal(new_section)
                legal = legal * new_section_is_legal
            
            if legal:
                out.append(v)
        return out
    
    def square_moves(board):
        """
        Given a board, returns a list of tuples
        The first value is an index, the second value
        is the list of legal moves for that index.
        
        It will only have a tuple for an index if the
        square at that index is currently empty.
        
        To optimize the sudoku search, the list is sorted
        (increasing) by the number of legal moves.
        """
        unsorted_legal_list = []
        for i in range(81):
            if board[i] == 0:
                legal_move_list = legal_moves(board, i)
                index_legal_move_list = (i, legal_move_list)
                unsorted_legal_list.append(index_legal_move_list)
        
        # to sort it, we transform it to another tuple with
        # the length of the legal list as the first element
        # and the tuple as the second element
        legal_list_for_sorting = []
        for index_legal_move_list in unsorted_legal_list:
            index, legal_move_list = index_legal_move_list
            legal_move_count = len(legal_move_list)
            sort_tuple = (legal_move_count, index_legal_move_list)
            legal_list_for_sorting.append(sort_tuple)
        
        # the sort
        legal_list_for_sorting.sort()
        
        # then we go back through and pull out just the second element
        # of the tuples we made for sorting
        out = []
        for legal_move_count, index_legal_move_list in legal_list_for_sorting:
            out.append(index_legal_move_list)
        return out
        
    def solve(board):
        """
        Recursively solves a sudoku by finding the set of possible moves,
        and trying them. Returns None if it finds a square with no legal moves,
        or if it is unable to find a winning board
        
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

        for index, moves in square_moves(board):
            if not moves:
                return None
            
            for move in moves:
                new_board = make_move(board, index, move)
                solved = solve(new_board)
                if solved is not None:
                    return solved
        return None
        
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
    
    solved = solve(board)
    if not confirm(solved):
        print "INVALID!!!!!"

    for row in [[solved[i] for i in d] for d in dex_gen(row)]:
        print row
        
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()

    solved = solve(board)
    if not confirm(solved):
        print "INVALID!!!!!"

    for row in [[solved[i] for i in d] for d in dex_gen(row)]:
        print row

    # unrolled()
    
