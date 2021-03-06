import random
import copy
from heapq import heappush, heappop


###Helper function outside of the class definition that takes a board
###and prints it out.
###Outside of the class definition
def pretty_print_2(size, board):
    for row in range(0, size):
        for col in range(0, size):
            print(board[row][col]),
        print " "
    print ""


###Creates a tuple out of a board represented as a list of lists.
###This is helpful as a tuple is hashable.
###Outside of the class definition
def linearize(board):
    a = tuple(board[0])
    for row in range(1, len(board)):
        a = a + tuple(board[row])
    return a


class Puzzle:
    def __init__(self, size):
        #create instances variables
        self.size = size  #size of the board
        self.squares = []  #board state
        self.my_goal = []  #solved state
        self.g = 0  #Length of path.

        count = 1
        ###Create the goal state.
        for i in range(0, size):
            my_row = []
            for j in range(0, size):
                if (i == size - 1 and j == size - 1):
                    my_row.append(-1)
                else:
                    my_row.append(count)
                count += 1
            self.my_goal.append(my_row)
        ###Randomize a board by populating it with the integers -1 and 1 through
        ###size * size -1, inclusive.
        so_far = []
        cur = -1
        taxi_cab = -1
        for i in range(0, size):
            my_row = []
            for j in range(0, size):
                while True:
                    cur = random.randint(0, size * size - 1)
                    if not cur in so_far:
                        break
                so_far.append(cur)
                if cur != 0:
                    my_row.append(cur)
                else:
                    my_row.append(-1)
            self.squares.append(my_row)
        #ensures we have an (even) solvable puzzle
        if self.invariant() % 2 != 0:
            self.switch_not_blank()

    #movement methods return a touple of the boolean sucess of the move
    #and a new puzzle *object* if returns false.
    #Up is defined as moving the blank up one square, down is the reverse, etc.
    #Definitions don't matter too much so long as they are consistent.
    def down(self):
        for row in range(0, self.size - 1):
            for col in range(0, self.size):
                if self.squares[row][col] == -1:
                    ans = copy.deepcopy(self)
                    ans.squares[row][col] = ans.squares[row + 1][col]
                    ans.squares[row + 1][col] = -1
                    return (True, ans)
        return (False, self)

    def up(self):
        for row in range(1, self.size):
            for col in range(0, self.size):
                if self.squares[row][col] == -1:
                    ans = copy.deepcopy(self)
                    ans.squares[row][col] = ans.squares[row - 1][col]
                    ans.squares[row - 1][col] = -1
                    return (True, ans)
        return (False, self)

    def left(self):
        for row in range(0, self.size):
            for col in range(1, self.size):
                if self.squares[row][col] == -1:
                    ans = copy.deepcopy(self)
                    ans.squares[row][col] = ans.squares[row][col - 1]
                    ans.squares[row][col - 1] = -1
                    return (True, ans)
        return (False, self)

    def right(self):
        for row in range(0, self.size):
            for col in range(0, self.size - 1):
                if self.squares[row][col] == -1:
                    ans = copy.deepcopy(self)
                    ans.squares[row][col] = ans.squares[row][col + 1]
                    ans.squares[row][col + 1] = -1
                    return (True, ans)
        return (False, self)

    #returns the number of cycles of the board
    def board_parity(self):
        #doesn't count the last cycle since the
        #list will be full, so start at 1
        count = 0

        #a basic list of numbers used to make
        #a permutation
        basic = []
        for i in range(1, self.size * self.size):
            basic.append(i)
        basic.append(-1)

        #list form of the board
        list_form = []
        for row in range(0, self.size):
            for col in range(0, self.size):
                list_form.append(self.squares[row][col])

        # print list_form, '\n', basic

        #the list of all the visted squares, stop when we've hit every number
        visited = []
        curNum = list_form[0]

        #move through it until you've hit all the numbers
        while len(visited) < self.size * self.size:
            #loop through until we find a cycle
            for i in range(self.size * self.size):
                if curNum in visited:
                    #complete cycle, up counter
                    count += 1
                    #find a number not in any previous cycle
                    for j in range(self.size * self.size):
                        if list_form[j] not in visited:
                            curNum = list_form[j]
                            break
                    break
                else:
                    #continue moving through the cycle
                    visited.append(curNum)
                    new_Index = list_form.index(curNum)
                    curNum = basic[new_Index]

        #in the case that it's one long cycle, it doesn't get counted
        #so compensate for this
        if count == 0:
            return 1
        return count

    #returns a tuple of the position of the blank, zero indexed
    def find_blank(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.squares[row][col] == -1:
                    return (row, col)

    #returns the taxicab distance of the blank
    #from the lower right corner
    def taxicab(self):
        return (self.size - 1 * -self.find_blank()[0]) - (
            self.size - 1 - self.find_blank()[1])

    #returns the invariant number associatied with
    #the board
    def invariant(self):
        return self.taxicab() + self.board_parity()

    #switches two tiles on the board with each other,
    #neither of which are the blank
    def switch_not_blank(self):
        #if neither of the first two are the blank, switch them
        if self.squares[0][0] != -1 and self.squares[0][1] != -1:
            store = self.squares[0][0]
            self.squares[0][0] = self.squares[0][1]
            self.squares[0][1] = store
        #otherwise switch the other two
        else:
            store = self.squares[1][0]
            self.squares[1][0] = self.squares[1][1]
            self.squares[1][1] = store

    #helper function that prints the state of the board.
    def pretty_print(self):
        for row in range(0, self.size):
            for col in range(0, self.size):
                print(self.squares[row][col]),
            print " "
        print ""

    #returns a list of legal square states, full puzzle object is passed
    def get_moves(self):
        #returns a list of possible moves, in the form of puzzle objects
        legal_moves = []
        move = self.right()
        #tests the boolean return
        if move[0]:
            #adds the changed board
            legal_moves.append(move[1])
        move = self.left()
        if move[0]:
            legal_moves.append(move[1])
        move = self.up()
        if move[0]:
            legal_moves.append(move[1])
        move = self.down()
        if move[0]:
            legal_moves.append(move[1])
        return legal_moves

    #A heuristic for determining how far the board state is from the goal state.
    #It returns the number of misplaced tiles, not counting the blank square.
    def h1(self):
        count = 0
        cur = -1
        for row in range(0, self.size):
            for col in range(0, self.size):
                cur = self.squares[row][col]
                if (cur != -1 and cur != row * self.size + col + 1):
                    count += 1
        return count

    #A heuristic for determining how far the board state is from the goal state.
    #Returns the sum of the manhattan distances, defined as far how a square is
    #from its goal state.
    def h2(self):
        count = 0
        proper_row = 0
        proper_col = 0
        cur = -1
        for row in range(0, self.size):
            for col in range(0, self.size):
                cur = self.squares[row][col]
                if cur != -1:
                    proper_row = (cur - 1) / self.size
                    proper_col = (cur - 1) % self.size
                    count += abs(proper_row - row)
                    count += abs(proper_col - col)
        return count

    #A heuristic for determining how far the board state is from the
    #Goal state.  Returns the number of swaps between the blank square and any
    #square needed to get to the goal state - a "relaxed" version of the 8-puzzle
    def h3(self):
        board = copy.deepcopy(self.squares)
        count = 0
        row_b = 0
        col_b = 0
        while (True):
            if board == self.my_goal:
                return count
            for row in range(self.size):
                for col in range(self.size):
                    if board[row][col] == -1:
                        row_b = row
                        col_b = col
            has_swapped = False
            if row_b == self.size - 1 and col_b == self.size - 1:
                for row in range(self.size):
                    for col in range(self.size):
                        if board[row][col] != self.size * row + col + 1:
                            if not has_swapped:
                                board[row_b][col_b] = board[row][col]
                                board[row][col] = -1
                                has_swapped = True
            else:
                to_find = row_b * self.size + col + 1
                for row in range(self.size):
                    for col in range(self.size):
                        if board[row][col] == self.size * row_b + col_b + 1:
                            if not has_swapped:
                                board[row_b][col_b] = board[row][col]
                                board[row][col] = -1
                                has_swapped = True
            count += 1
        return count

    #A* algorithm, takes a starting point and integer 1,2, or 3
    #that defines the heuristic to use
    def search(self, num_h):
        #use to ensure we don't enter an infinte loop
        #set
        past_states = {linearize(self.squares)}
        #priorityQueue, made g an instance varaible of the board
        heap = []  #f(n), puzzle object

        #inialize
        h = 0
        if num_h == 1:
            h = self.h1()
        if num_h == 2:
            h = self.h2()
        if num_h == 3:
            h = self.h3()

        init_heap_tuple = (h, self)
        heappush(heap, init_heap_tuple)
        #while there's stuff in the heap
        count = 1
        while heap:

            best_move = heappop(heap)
            if best_move[1].squares == self.my_goal:
                return (True, best_move[1].g, count)
            else:
                sucessors = best_move[1].get_moves()
                for s in sucessors:
                    if linearize(s.squares) not in past_states:
                        count += 1
                        past_states.add(linearize(s.squares))

                        s.g = best_move[1].g + 1

                        if num_h == 1:
                            heappush(heap, (s.g + s.h1(), s))
                        if num_h == 2:
                            heappush(heap, (s.g + s.h2(), s))
                        if num_h == 3:
                            heappush(heap, (s.g + s.h3(), s))
            if not heap:
                best_move[1].pretty_print()
        #if heap empties, then we have failed

        return (False, [[]], -1)


##testing
##constants
my_depth = 16
puzzles_to_solve = 100
num_heuristic = 2
size_puzzle = 3
#set up the dictionary of results.  Key is depth of solution
results = {}
results[my_depth] = (0, 0)

print'hello world'

while (True):
    puzzle = Puzzle(size_puzzle)
    result = puzzle.search(num_heuristic)
    depth = result[1]
    if depth != my_depth:
        continue
    node = result[2]
    times_solved = results[depth][0]
    if times_solved < puzzles_to_solve:
        total_node_count = results[depth][1]
        entry = {depth: (times_solved + 1, total_node_count + node)}
        results.update(entry)
        continue
    break
print results
