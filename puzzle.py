import random
import heapq


class Puzzle:

    squares = []
    size = -1

    def __init__(self, size):
        self.size = size
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
                    # taxi_cab = size - i + size - j - 2
                    # print "taxi cab: "
                    # print taxi_cab
            self.squares.append(my_row)
        #ensures we have an (odd) solvable puzzle
        if self.invariant() % 2 == 0:
            self.switch_not_blank()

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

        #the list of all the visted ones, stop when we've hit every number
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

    #returns a tuple of the position of the blank
    def find_blank(self):
        for row in range(0, self.size):
            for col in range(0, self.size):
                if self.squares[row][col] == -1:
                    return (row, col)

    #returns the taxicab distance of the blank
    #from the lower right corner
    def taxicab(self):
        return (self.size - 1) * 2 - self.find_blank()[0] - self.find_blank()[1]

    #returns the invariant number associatied with
    #the board
    def invariant(self):
        return self.taxicab() + self.board_parity()

    #switches two tiles on the board with each other,
    #neither of which are the blank
    def switch_not_blank(self):
        if self.squares[0][0] != -1 and self.squares[0][1] != -1:
            store = self.squares[0][0]
            self.squares[0][0] = self.squares[0][1]
            self.squares[0][1] = store
        else:
            store = self.squares[1][0]
            self.squares[1][0] = self.squares[1][1]
            self.squares[1][1] = store

    def get_state(self):
        return squares

    def down(self):
        for row in range(0, self.size - 1):
            for col in range(0, self.size):
                if (self.squares[row][col] == -1):
                    self.squares[row][col] = self.squares[row + 1][col]
                    self.squares[row + 1][col] = -1
                    return True
        return False

    def up(self):
        for row in range(1, self.size):
            for col in range(0, self.size):
                if (self.squares[row][col] == -1):
                    self.squares[row][col] = self.squares[row - 1][col]
                    self.squares[row - 1][col] = -1
                    return True
        return False

    def left(self):
        for row in range(0, self.size):
            for col in range(1, self.size):
                if (self.squares[row][col] == -1):
                    self.squares[row][col] = self.squares[row][col - 1]
                    self.squares[row][col - 1] = -1
                    return True
        return False

    def right(self):
        for row in range(0, self.size):
            for col in range(0, self.size - 1):
                if (self.squares[row][col] == -1):
                    self.squares[row][col] = self.squares[row][col + 1]
                    self.squares[row][col + 1] = -1
                    return True
        return False

    def pretty_print(self):
        for row in range(0, self.size):
            for col in range(0, self.size):
                print(self.squares[row][col]),
            print " "
        print ""

    def h1(self, board):
        count = 0
        cur = -1
        for row in range(0, self.size):
            for col in range(0, self.size):
                cur = board[row][col]
                if (cur != -1 and cur != row * self.size + col + 1):
                    count += 1
        return count

    def h2(self, board):
        count = 0
        proper_row = 0
        proper_col = 0
        cur = -1
        for row in range(0, self.size):
            for col in range(0, self.size):
                cur = board[row][col]
                if cur != -1:
                    proper_row = (cur - 1) / self.size
                    proper_col = (cur - 1) % self.size
                    count += abs(proper_row - row)
                    count += abs(proper_col - col)
        return count

    def get_moves(self, board):
        return True

    def search(self, is_h1):
        past_states = []
        heap = []
        for move in get_moves:
            if is_h1:
                heappush(heap, (h1(move), ))


##testing

#why are these the same???
puzzle = Puzzle(3)
puzzle.pretty_print()
#this will always be odd now
print 'invariant', puzzle.invariant()
# puzzle1 = Puzzle(4)
# puzzle.pretty_print()

# counter1 = 0
# counter2 = 0
# counter3 = 0
# counter4 = 0
# counter5 = 0
# counter6 = 0
# counter7 = 0
# counter8 = 0
#why does this create the same puzzle 10,000 times instead of 10,000 different puzzles?
# for i in range(10000):
#     puzzle = Puzzle(3)
#     puzzle.pretty_print()
#     if puzzle.find_board_parity() == 1:
#         counter1 +=1
#     if puzzle.find_board_parity() == 2:
#         counter2 +=1
#     if puzzle.find_board_parity() == 3:
#         counter3 +=1
#     if puzzle.find_board_parity() == 4:
#         counter4 +=1
#     if puzzle.find_board_parity() == 5:
#         counter5 +=1
#     if puzzle.find_board_parity() == 6:
#         counter6 +=1
#     if puzzle.find_board_parity() == 7:
#         counter7 +=1
#     if puzzle.find_board_parity() == 8:
#         counter8 +=1
#
# print counter1, counter2, counter3, counter4, counter5, counter6, counter7, counter8,
