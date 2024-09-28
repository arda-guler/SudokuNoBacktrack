# No-backtrack sudoku solver
#
# It's made to be more human-like than the
# backtracking method, because average person does not
# like using erasers whether on paper or in mind.
#
# It can't solve everything but it can likely solve
# everything up to the most difficult ones.
#
# ...in which case you can just use sth like this as
# a 'preconditioner' for a backtrack solver.

from copy import deepcopy

class Cell:
    def __init__(self, i, j, num=0):
        self.i = i
        self.j = j
        self.num = num

        if j < 3:
            if i < 3:
                self.box = 0
            elif 3 <= i < 6:
                self.box = 1
            else:
                self.box = 2
        elif 3 <= j < 6:
            if i < 3:
                self.box = 3
            elif 3 <= i < 6:
                self.box = 4
            else:
                self.box = 5
        else:
            if i < 3:
                self.box = 6
            elif 3 <= i < 6:
                self.box = 7
            else:
                self.box = 8

class SudokuGame:
    def __init__(self, board):
        self.setup_board(board)
        self.prev_board = deepcopy(self.board)

    def setup_board(self, board):
        nums = board
        mng_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        for j in range(9):
            for i in range(9):
                mng_board[j][i] = Cell(i, j, nums[j][i])

        self.board = mng_board

    def getNumbersInBox(self, boxnum):
        nums = []
        for i in range(9):
            for j in range(9):
                if self.board[j][i].box == boxnum:
                    if self.board[j][i].num != 0:
                        nums.append(self.board[j][i].num)

        return nums

    def getNumbersInRow(self, row):
        j = row
        nums = []
        for i in range(9):
            if self.board[j][i].num != 0:
                nums.append(self.board[j][i].num)

        return nums

    def getNumbersInColumn(self, column):
        i = column
        nums = []
        for j in range(9):
            if self.board[j][i].num != 0:
                nums.append(self.board[j][i].num)

        return nums

    def getAvailableNumbers(self, x, y):
        if self.board[y][x].num != 0:
            return []
        
        all_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        nums_row = self.getNumbersInRow(y)
        nums_column = self.getNumbersInColumn(x)
        nums_box = self.getNumbersInBox(self.board[y][x].box)

        unavailable_nums = set(nums_box) | set(nums_row) | set(nums_column)
        available_nums = set(all_nums) - unavailable_nums
        
        return list(available_nums)

    def findAllAvailableNumbers(self):
        # i love tensors hell yea
        self.available_nums = [[[], [], [], [], [], [], [], [], []],
                               [[], [], [], [], [], [], [], [], []],
                               [[], [], [], [], [], [], [], [], []],
                               [[], [], [], [], [], [], [], [], []],
                               [[], [], [], [], [], [], [], [], []],
                               [[], [], [], [], [], [], [], [], []],
                               [[], [], [], [], [], [], [], [], []],
                               [[], [], [], [], [], [], [], [], []],
                               [[], [], [], [], [], [], [], [], []]]
        
        for j in range(9):
            for i in range(9):
                self.available_nums[j][i] = self.getAvailableNumbers(i, j)

    def filterAvailableNumbers(self):
        for b in range(9):
            # check 'must' rows
            onerows = []
            tworows = []
            threerows = []
            fourrows = []
            fiverows = []
            sixrows = []
            sevenrows = []
            eightrows = []
            ninerows = []

            for j in range(9):
                for i in range(9):
                    if self.board[j][i].box == b:
                        if 1 in self.available_nums[j][i]:
                            onerows.append(j)
                        if 2 in self.available_nums[j][i]:
                            tworows.append(j)
                        if 3 in self.available_nums[j][i]:
                            threerows.append(j)
                        if 4 in self.available_nums[j][i]:
                            fourrows.append(j)
                        if 5 in self.available_nums[j][i]:
                            fiverows.append(j)
                        if 6 in self.available_nums[j][i]:
                            sixrows.append(j)
                        if 7 in self.available_nums[j][i]:
                            sevenrows.append(j)
                        if 8 in self.available_nums[j][i]:
                            eightrows.append(j)
                        if 9 in self.available_nums[j][i]:
                            ninerows.append(j)

            allrows = [onerows, tworows, threerows, fourrows, fiverows, sixrows, sevenrows, eightrows, ninerows]
            for i in range(9):
                allrows[i] = list(set(allrows[i]))

            for idxm1, crow in enumerate(allrows):
                idx = idxm1 + 1
                if len(crow) == 1:
                    horizboxes = self.getNeighboringBoxesHorizontal(b)

                    for b2 in horizboxes:
                        j = crow[0]
                        for i in range(9):
                            if self.board[j][i].box == b2 and (idx in self.available_nums[j][i]):
                                self.available_nums[j][i].remove(idx)

            # check 'must' columns
            onecols = []
            twocols = []
            threecols = []
            fourcols = []
            fivecols = []
            sixcols = []
            sevencols = []
            eightcols = []
            ninecols = []

            for j in range(9):
                for i in range(9):
                    if self.board[j][i].box == b:
                        if 1 in self.available_nums[j][i]:
                            onecols.append(i)
                        if 2 in self.available_nums[j][i]:
                            twocols.append(i)
                        if 3 in self.available_nums[j][i]:
                            threecols.append(i)
                        if 4 in self.available_nums[j][i]:
                            fourcols.append(i)
                        if 5 in self.available_nums[j][i]:
                            fivecols.append(i)
                        if 6 in self.available_nums[j][i]:
                            sixcols.append(i)
                        if 7 in self.available_nums[j][i]:
                            sevencols.append(i)
                        if 8 in self.available_nums[j][i]:
                            eightcols.append(i)
                        if 9 in self.available_nums[j][i]:
                            ninecols.append(i)

            allcols = [onecols, twocols, threecols, fourcols, fivecols, sixcols, sevencols, eightcols, ninecols]
            for i in range(9):
                allcols[i] = list(set(allcols[i]))

            for idxm1, ccol in enumerate(allcols):
                idx = idxm1 + 1
                if len(ccol) == 1:
                    vertboxes = self.getNeighboringBoxesVertical(b)

                    for b2 in vertboxes:
                        i = ccol[0]
                        for j in range(9):
                            if self.board[j][i].box == b2 and (idx in self.available_nums[j][i]):
                                self.available_nums[j][i].remove(idx)


    def fillSinglePossibilities(self):
        for j in range(9):
            for i in range(9):
                if self.board[j][i].num == 0:
                    if len(self.available_nums[j][i]) == 1:
                        self.board[j][i].num = self.available_nums[j][i][0]

    def fillSingleRowPossibilities(self):
        for j in range(9):
            ones = []
            twos = []
            threes = []
            fours = []
            fives = []
            sixes = []
            sevens = []
            eights = []
            nines = []

            for i in range(9):
                if 1 in self.available_nums[j][i]:
                    ones.append(i)
                if 2 in self.available_nums[j][i]:
                    twos.append(i)
                if 3 in self.available_nums[j][i]:
                    threes.append(i)
                if 4 in self.available_nums[j][i]:
                    fours.append(i)
                if 5 in self.available_nums[j][i]:
                    fives.append(i)
                if 6 in self.available_nums[j][i]:
                    sixes.append(i)
                if 7 in self.available_nums[j][i]:
                    sevens.append(i)
                if 8 in self.available_nums[j][i]:
                    eights.append(i)
                if 9 in self.available_nums[j][i]:
                    nines.append(i)

            if len(ones) == 1:
                self.board[j][ones[0]].num = 1
            if len(twos) == 1:
                self.board[j][twos[0]].num = 2
            if len(threes) == 1:
                self.board[j][threes[0]].num = 3
            if len(fours) == 1:
                self.board[j][fours[0]].num = 4
            if len(fives) == 1:
                self.board[j][fives[0]].num = 5
            if len(sixes) == 1:
                self.board[j][sixes[0]].num = 6
            if len(sevens) == 1:
                self.board[j][sevens[0]].num = 7
            if len(eights) == 1:
                self.board[j][eights[0]].num = 8
            if len(nines) == 1:
                self.board[j][nines[0]].num = 9

    def fillSingleColumnPossibilities(self):
        for i in range(9):
            ones = []
            twos = []
            threes = []
            fours = []
            fives = []
            sixes = []
            sevens = []
            eights = []
            nines = []

            for j in range(9):
                if 1 in self.available_nums[j][i]:
                    ones.append(j)
                if 2 in self.available_nums[j][i]:
                    twos.append(j)
                if 3 in self.available_nums[j][i]:
                    threes.append(j)
                if 4 in self.available_nums[j][i]:
                    fours.append(j)
                if 5 in self.available_nums[j][i]:
                    fives.append(j)
                if 6 in self.available_nums[j][i]:
                    sixes.append(j)
                if 7 in self.available_nums[j][i]:
                    sevens.append(j)
                if 8 in self.available_nums[j][i]:
                    eights.append(j)
                if 9 in self.available_nums[j][i]:
                    nines.append(j)

            if len(ones) == 1:
                self.board[ones[0]][i].num = 1
            if len(twos) == 1:
                self.board[twos[0]][i].num = 2
            if len(threes) == 1:
                self.board[threes[0]][i].num = 3
            if len(fours) == 1:
                self.board[fours[0]][i].num = 4
            if len(fives) == 1:
                self.board[fives[0]][i].num = 5
            if len(sixes) == 1:
                self.board[sixes[0]][i].num = 6
            if len(sevens) == 1:
                self.board[sevens[0]][i].num = 7
            if len(eights) == 1:
                self.board[eights[0]][i].num = 8
            if len(nines) == 1:
                self.board[nines[0]][i].num = 9

    def areAllCellsFilled(self):
        filled = True
        for j in range(9):
            for i in range(9):
                if self.board[j][i].num == 0:
                    filled = False
                    break

        return filled

    def printBoard(self):
        for j in range(9):
            for i in range(9):
                print(self.board[j][i].num, end="")
            print("")

    def printBoardWithChanges(self):
        for j in range(9):
            for i in range(9):
                if self.board[j][i].num == self.prev_board[j][i].num:
                    print(" " + str(self.board[j][i].num) + " ", end="")
                else:
                    print(">" + str(self.board[j][i].num) + "<", end="")

            print("")

        self.prev_board = deepcopy(self.board)
     
    def getNeighboringBoxesVertical(self, box):
        v1 = [0, 3, 6]
        v2 = [1, 4, 7]
        v3 = [2, 5, 8]

        if box in v1:
            v1.remove(box)
            return v1
        elif box in v2:
            v2.remove(box)
            return v2
        else:
            v3.remove(box)
            return v3

    def getNeighboringBoxesHorizontal(self, box):
        h1 = [0, 1, 2]
        h2 = [3, 4, 5]
        h3 = [6, 7, 8]

        if box in h1:
            h1.remove(box)
            return h1
        elif box in h2:
            h2.remove(box)
            return h2
        else:
            h3.remove(box)
            return h3

game = [[0, 3, 2, 6, 0, 5, 4, 7, 0],
        [5, 0, 0, 0, 3, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 8],
        [2, 5, 0, 0, 0, 0, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 6],
        [8, 0, 0, 9, 2, 0, 0, 0, 5],
        [0, 2, 0, 5, 0, 0, 0, 1, 3],
        [0, 0, 0, 3, 0, 0, 6, 0, 7],
        [0, 8, 0, 0, 9, 7, 0, 5, 4]]

##inrows = []
##print("Enter each row and press enter.")
##print("Place NO symbols or spaces between cells.")
##print("Use '0' for empty cells.")
##print("e.g. a valid row: 090018006\n\n")
##for j in range(9):
##    exp_str = "Enter Row " + str(j+1) + ":"
##    inrow_str = input(exp_str)
##    intlist = [int(char) for char in inrow_str]
##    inrows.append(intlist)

print("== NO-BACKTRACK SUDOKU SOLVER ==")
print("'0' denotes an empty cell.\n")
sudoku = SudokuGame(game)
print("Initial state:")
sudoku.printBoard()

MAX_ITER = 20
for i in range(MAX_ITER):
    sudoku.findAllAvailableNumbers()
    sudoku.filterAvailableNumbers()
    sudoku.fillSinglePossibilities()
    sudoku.fillSingleColumnPossibilities()
    sudoku.fillSingleRowPossibilities()

    print("")
    print("Iteration " + str(i))
    sudoku.printBoardWithChanges()
    input("Press Enter to continue...")

    if sudoku.areAllCellsFilled():
        break

print("\nResult:")
sudoku.findAllAvailableNumbers()
sudoku.filterAvailableNumbers()
sudoku.printBoard()

if not sudoku.areAllCellsFilled():
    print("")
    print("Not all cells could be found without backtracking. Here are possibilities for remaining cells:")
    for r in sudoku.available_nums:
        print(r)

input("\nPress Enter to quit...")
