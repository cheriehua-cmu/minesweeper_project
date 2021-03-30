########################
#Name: Cherie Hua
#AndrewID: cxhua
#Section: O
#######################
import sys, math, copy, string, random, time
from cmu_112_graphics import * # copied (with modifications) from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from fractions import Fraction #from https://docs.python.org/3.1/library/fractions.html
from tkinter import *
#from PIL import Image

class Game(App):
    #will separate these functions later
    def appStarted(self):
        #some modes
        self.beginner = (9, 9, 10)
        self.intermediate = (16, 16, 40)
        self.expert = (16, 30, 99)
        #set dimensions here
        self.rows = 4
        self.cols = 4
        self.mines = 0
        self.margin = self.height//25
        self.teacherWidth = self.width//3
        self.instructionsHeight = self.height // 7
        self.gridWidth  = self.width - 2*self.margin - self.teacherWidth
        self.gridHeight = self.height - 2*self.margin - self.instructionsHeight
        self.cellWidth  = self.gridWidth // self.cols
        self.cellHeight = self.gridHeight // self.rows
        #creates base board
        #here's a hardcoded board I used for testing, set rows and cols = 4 and mines = 0 to use this
        self.board = [[0, '*', 0, '*'],[0, 0, 0, 0],[0, 0, 0, 0],[0, '*', '*', 0]]
        #self.board = [([0] * self.cols) for row in range(self.rows)]
        #creates a cover that the player can click to uncover
        self.cover = [([True] * self.cols) for row in range(self.rows)]
        self.lost = False
        self.won = False
        self.canClick = True
        self.firstClick = True
        self.probabilities = [([None] * self.cols) for row in range(self.rows)]
        self.getProbabilities = False
        self.reducedProbabilities = copy.deepcopy(self.probabilities)
        self.moves = []
        self.moves.append(copy.deepcopy(self.cover))
        self.AIScroll = False
        self.movePlace = 0
        self.endScreen = None
        self.getStrategies = False
        self.pattern = None

    def generateMines(self):
        #generates mines randomly until the number of mines generated equals the number
        #the player requested
        numMines = 0
        while numMines < self.mines:
            row = random.randint(0, self.rows)-1
            col = random.randint(0, self.cols)-1
            if self.board[row][col] != '*' and self.board[row][col] != 'clear':
                self.board[row][col] = '*'
                numMines += 1

    def placeNumbers(self):
        #loop through every space in the board
        for row in range(self.rows):
            for col in range(self.cols):
                #if the space has a mine
                if self.board[row][col] == 'clear':
                    self.board[row][col] = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == '*':
                    #add 1 to the numbers around the mine
                    for drow in [-1, 0, 1]:
                        for dcol in [-1, 0, 1]:
                            if (drow, dcol) == (0, 0):
                                continue
                            checkRow = row+drow
                            checkCol = col+dcol
                            if (checkRow < self.rows and checkCol < self.cols 
                                and checkRow >= 0 and checkCol >= 0 and 
                                self.board[checkRow][checkCol] != '*'):
                                self.board[checkRow][checkCol] += 1

    def mousePressed(self, event):
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        (row, col) = Game.getCell(self, event.x, event.y)
        AILeft = self.width - self.teacherWidth + self.margin*2
        AITop = self.height//8
        AIRight = self.width - self.margin*2
        AIBottom = self.height//5
        if (event.x > AILeft and event.x < AIRight and event.y < AIBottom and event.y > AITop
            and (self.lost == True or self.won == True)):
            self.AIScroll = True
            self.cover = [([True] * self.cols) for row in range(self.rows)]
            self.lost = False
            self.won = False
        if (row, col) != (-1, -1) and self.canClick:
            if self.firstClick:
                Game.firstClick(self, row, col)
            if self.cover[row][col] == 'flag':
                return
            if self.cover[row][col] != 'flag':
                self.cover[row][col] = False
            if (self.cover[row][col] == False and self.board[row][col] != '*' 
                and self.board[row][col] > 0):
                Game.clearWithNumberPress(self, row, col)
            if self.board[row][col] == '*' and self.cover[row][col] != 'flag':
                Game.revealMines(self)
                self.lost = True
                self.canClick = False
            Game.expand(self, row, col)
        if self.getProbabilities and self.probabilities[row][col] != None:
            pattern = Game.isPattern(self, row, col)
            Game.getExplanation(self, pattern)
        

    def clearWithNumberPress(self, row, col):
        if Game.checkAround(self, row, col, 'flag', self.cover) == self.board[row][col]:
            for drow in [-1, 0, 1]:
                for dcol in [-1, 0, 1]:
                    if (drow, dcol) == (0, 0):
                        continue
                    checkRow = row+drow
                    checkCol = col+dcol
                    if (checkRow < self.rows and checkCol < self.cols 
                        and checkRow >= 0 and checkCol >= 0 and 
                        self.cover[checkRow][checkCol] != 'flag'):
                            self.cover[checkRow][checkCol] = False
                            if self.board[checkRow][checkCol] == '*':
                                Game.revealMines(self)
                                self.lost = True
                                self.canClick = False

    def checkAround(self, row, col, thing, place):
        number = 0
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if (drow, dcol) == (0, 0):
                    continue
                checkRow = row+drow
                checkCol = col+dcol
                if (checkRow < self.rows and checkCol < self.cols 
                    and checkRow >= 0 and checkCol >= 0 and place[checkRow][checkCol] == thing
                    and (drow, dcol) != (0, 0)):
                    number += 1
        return number

    def firstClick(self, row, col):
        #clears a larger then 1 block space on the first click
        self.firstClick = False
        #clear a square no matter what the dimensions are
        # rowOrCol = min(self.rows, self.cols)
        # clearRows = rowOrCol//6 + 1
        # clearCols = rowOrCol//6 + 1
        # for clearRow in range(row-clearRows, row+clearRows):
        #     for clearCol in range(col-clearCols, col+clearCols):
        #         if (clearRow < self.rows and clearCol < self.cols 
        #             and clearRow >= 0 and clearCol >= 0):
        #             self.board[clearRow][clearCol] = 'clear'
        Game.generateMines(self)
        Game.placeNumbers(self)

    def expand(self, r, c):
        self.cover[r][c] = False
        allClear = False
        while allClear == False:
            clearSpaces = 0
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.board[row][col] == 0 and self.cover[row][col] == False:
                        for drow in [-1, 0, 1]:
                            for dcol in [-1, 0, 1]:
                                if (drow, dcol) == (0, 0):
                                    continue
                                checkRow = row+drow
                                checkCol = col+dcol
                                if (checkRow < self.rows and checkCol < self.cols 
                                    and checkRow >= 0 and checkCol >= 0):
                                    if (self.board[checkRow][checkCol] != '*' and 
                                        self.cover[checkRow][checkCol] == True):
                                        self.cover[checkRow][checkCol] = False
                                        clearSpaces += 1
            if clearSpaces == 0:
                allClear = True

    def rightMousePressed(self, event):
        #edited cmu_112_graphics.py to include right clicking, bounded to <Button-2>
        #from what I've seen online, right clicking is usually Button 3, and only Button 2 for OS X
        #so it may not work for non-Mac users
        (row, col) = Game.getCell(self, event.x, event.y)
        if self.cover[row][col] != 'flag' and self.canClick and self.cover[row][col]:
            self.cover[row][col] = 'flag'
        elif self.cover[row][col] == 'flag' and self.canClick:
            self.cover[row][col] = True

    def getCellBounds(self, row, col):
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        columnWidth = self.gridWidth // self.cols
        rowHeight = self.gridHeight // self.rows
        x0 = self.margin + col * columnWidth
        x1 = self.margin + (col+1) * columnWidth
        y0 = self.margin + self.instructionsHeight + row * rowHeight
        y1 = self.margin + self.instructionsHeight + (row+1) * rowHeight
        return (x0, y0, x1, y1)

    def pointInGrid(self, x, y):
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        return ((self.margin <= x <= self.width-self.margin-self.teacherWidth) and
                (self.margin + self.instructionsHeight <= y <= self.height-self.margin))
    
    def getCell(self, x, y):
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        if not Game.pointInGrid(self, x, y):
            return (-1, -1)
        row = int((y - self.margin - self.instructionsHeight) // self.cellHeight)
        col = int((x - self.margin) // self.cellWidth)
        return (row, col)

    def win(self):
        #if every non-mine space is cleared, then set win to True and stop the player
        #from playing any more
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != '*' and self.cover[row][col] == True:
                    return False
        Game.revealMines(self)
        self.canClick = False
        self.won = True
        return True

    def revealMines(self):
        #remove cover when the board has a mine
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == '*' and self.cover[row][col] != 'flag':
                    self.cover[row][col] = False
                if self.cover[row][col] == 'flag' and self.board[row][col] != '*':
                    self.cover[row][col] = 'wrong'

    def timerFired(self):
        Game.win(self)
        Game.placeProbabilities(self)

    def tankSolver(self, partialBoard):
        (move, solution) = TankSolver(partialBoard).solve()
        solutions = []
        if solution != None:
            for i in range(len(solution)):
                solutions.append(solution[i].minePositions)
            return solutions

    def keyPressed(self, event):
        #go to next move
        if event.key == 'p':
            if self.getProbabilities:
                self.getProbabilities = False
                self.canClick = True
            else:
                self.getProbabilities = True
                self.canClick = False
        if event.key == 's':
            if self.getStrategies:
                self.getStrategies = False
            else:
                self.getStrategies = True
        if self.AIScroll:
            if event.key == 'Right' and self.won == False and self.lost == False:
                Game.executeMove(self)
                if self.cover not in self.moves:
                    self.moves.append(copy.deepcopy(self.cover))
                self.movePlace += 1
                if self.movePlace >= len(self.moves):
                    return
                if self.endScreen != None and self.movePlace == self.endScreen[0]:
                        if self.endScreen[1] == 'lost':
                            self.lost = True
                        if self.endScreen[1] == 'won':
                            self.won = True
            if event.key == 'Left' and self.movePlace > 0:
                if self.lost:
                    self.lost = False
                    self.endScreen = (self.movePlace, 'lost')
                if self.won:
                    self.won = False
                    self.endScreen = (self.movePlace, 'won')
                self.movePlace -= 1

    def findMove(self):
        if self.firstClick:
            Game.firstClick(self, r, c)
            self.firstClick = False
            r = random.randint(0, self.rows)
            c = random.randint(0, self.cols)
            return (r, c)

        probs = copy.deepcopy(self.probabilities)
        for r in range(self.rows):
            for c in range(self.cols):
                if probs[r][c] == None or self.cover[r][c] == False:
                    probs[r][c] = 2

        minProb = min([min(value) for value in probs])
        
        for row in range(self.rows):
            for col in range(self.cols):
                if probs[row][col] == minProb:
                    (minRow, minCol) = (row, col)
        return (minRow, minCol)

    def executeMove(self):
        if self.won == False and self.lost == False:
            (row, col) = Game.findMove(self)
            self.cover[row][col] = False
            Game.expand(self, row, col)
            if self.board[row][col] == '*':
                self.lost = True
            win = True
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.cover[row][col] == True and self.board[row][col] != '*':
                        win = False
            if win:
                self.won = True

    def placeProbabilities(self):
        #look through every tile
        for row in range(self.rows):
            for col in range(self.cols):
                #if there's a revealed number
                if (type(self.board[row][col]) == int and self.board[row][col] > 0 
                    and self.cover[row][col] != True):
                    nUnrevealedTiles = Game.findUnrevealedTiles(self, row, col)
                    #place 1 if the number of tiles equals the number of mines
                    if nUnrevealedTiles == self.board[row][col]:
                        Game.definiteZerosAndOnes(self, row, col, 1)
                    #place 0 for the rest of the tiles in the area surrounding the number
                    nUnrevealedTiles = Game.findUnrevealedTiles(self, row, col)
                    nRevealedMines = Game.checkAround(self, row, col, 1, self.probabilities)
                    if nRevealedMines == self.board[row][col] and nRevealedMines < nUnrevealedTiles:
                        Game.definiteZerosAndOnes(self, row, col, 0)
        partialBoard = Game.getPartialBoard(self)
        if partialBoard != None:
            positions = Game.tankSolver(self, partialBoard)
            Game.getAIProbabilities(self, positions)

    def getAIProbabilities(self, positions):
        if positions == []:
            return
        rows = len(positions[0])
        if len(positions) == 1:
            for state in positions:
                for row in range(rows):
                    cols = len(state[row])
                    for col in range(cols):
                        r = state[row][col][0]
                        c = state[row][col][1]
                        value = state[row][col][2]
                        if value == 'True':
                            self.probabilities[r][c] = 1
                        else:
                            self.probabilities[r][c] = 0
        else:
            #add 1 to partialProbabilities if there's a mine in that location for each state
            partialProbabilities = [[None]*self.cols for rows in range(self.rows)] 
            for state in positions:
                for row in range(rows):
                    cols = len(state[row])
                    for col in range(cols):
                        r = state[row][col][0]
                        c = state[row][col][1]
                        if state[row][col][2] == 'True':
                            if partialProbabilities[r][c] == None:
                                partialProbabilities[r][c] = 0
                            partialProbabilities[r][c] += 1
            
            for row in range(self.rows):
                for col in range(self.cols):
                    if partialProbabilities[row][col] != None:
                        self.probabilities[row][col] = Fraction(partialProbabilities[row][col], len(positions))

    def getPartialBoard(self):
        partialCoords = []
        #go through everything in board
        for row in range(self.rows):
            for col in range(self.cols):
                #if it's a revealed number
                if (self.cover[row][col] == False and type(self.board[row][col]) == int 
                    and self.board[row][col] > 0):
                    #add it to partialCoords
                    partialCoords.append((row, col, self.board[row][col]))
                    #add everything around it to partialCoords too if it's a covered tile
                    for drow in [-1, 0, 1]:
                        for dcol in [-1, 0, 1]:
                            checkRow = row+drow
                            checkCol = col+dcol
                            if (checkRow < self.rows and checkCol < self.cols 
                                and checkRow >= 0 and checkCol >= 0 
                                and self.cover[checkRow][checkCol] != False
                                and (checkRow, checkCol, None) not in partialCoords
                                 and (drow, dcol) != (0, 0)):
                                if self.probabilities[checkRow][checkCol] == 1:
                                    partialCoords.append((checkRow, checkCol, 'True'))
                                else:
                                    partialCoords.append((checkRow, checkCol, None))
       
        partialCoords.sort(key = lambda tup: (tup[0], tup[1]))

        partialBoard = []
        rowList = []
        #go through everything in particalCoords and make it a 2D List
        for coords in range(len(partialCoords)):
            if coords > 0 and partialCoords[coords][0] != partialCoords[coords-1][0]:
                partialBoard.append(rowList)
                rowList = []
                rowList.append(partialCoords[coords])
            else:
                rowList.append(partialCoords[coords])
        partialBoard.append(rowList)

        if partialBoard != []:
            return partialBoard

    def definiteZerosAndOnes(self, row, col, thing):
        #place around the 8 squares around the number
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if (drow, dcol) == (0, 0):
                    continue
                checkRow = row+drow
                checkCol = col+dcol
                if (checkRow < self.rows and checkCol < self.cols 
                    and checkRow >= 0 and checkCol >= 0 and 
                    self.cover[checkRow][checkCol] and self.probabilities[checkRow][checkCol] != (1-thing)):
                        self.probabilities[checkRow][checkCol] = thing

    def findUnrevealedTiles(self, row, col):
        #count the number of covered tiles in the 8 squares surrounding a number
        nUnrevealedTiles = 0
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if (drow, dcol) == (0, 0):
                    continue
                checkRow = row+drow
                checkCol = col+dcol
                if (checkRow < self.rows and checkCol < self.cols
                    and checkRow >= 0 and checkCol >= 0 and self.cover[checkRow][checkCol] != False
                    and self.probabilities[checkRow][checkCol] != 0):
                    nUnrevealedTiles += 1
        return nUnrevealedTiles

    def getExplanation(self, pattern):
        #explanations copied from http://www.minesweeper.info/wiki/Strategy
        if pattern == '121':
            self.pattern = '''
Common pattern (121) - This 
is a variation of the 1-2 pattern.
There is 1 mine in the 
first two squares, and 
2 mines in the first three
 squares. The 3rd square over 
must be a mine. Apply this 
from the other direction as well.'''
            return
        if pattern == '1221':
            self.pattern = '''
Common pattern (1221) - 
This is a variation of the
 1-2 pattern.
There is 1 mine in the 
first two squares, and 
2 mines in the 
first three squares. 
The 3rd square over 
must be a mine. Apply this 
from the other 
direction as well.
'''
            return
        if pattern == '11':
            self.pattern = '''
There is 1 mine in the first
 two squares, and 1 mine in the 
first three squares. The 3rd 
square over must be empty.
'''
            return
        if pattern == '12':
            self.pattern = '''
There is 1 mine in the first 
two squares, and 2 mines in the 
first three squares. The 3rd square
 over must be a mine.
'''
            return
        if pattern == '?':
            self.pattern = '''
The number of solutions
 with a mine 
in this square divided 
by the total solutions.
        '''
            return
        else:
            self.pattern = '''
If a number is touching the same 
number of squares, then the
 squares are all mines.
'''
            return

    def isPattern(self, row, col):
        #modified from https://www.cs.cmu.edu/~112/notes/week5-case-studies.html#wordsearch1
        patterns = ['121', '1221', '11', '12']
        for pattern in patterns:
            dcol = 0
            for drow in [-1, +1]:
                result = Game.isPatternHelper(self, pattern, row, col, drow, dcol)
                if (result):
                    return pattern
            drow = 0
            for dcol in [-1, +1]:
                result = Game.isPatternHelper(self, pattern, row, col, drow, dcol)
                if (result):
                    return pattern
        return '?'

    def isPatternHelper(self, number, startRow, startCol, drow, dcol):
        #modified from https://www.cs.cmu.edu/~112/notes/week5-case-studies.html#wordsearch1
        number = number
        for i in range(len(number)):
            row = startRow + i*drow
            col = startCol + i*dcol
            if ((row < 0) or (row >= self.rows) or
                (col < 0) or (col >= self.cols) or
                str(self.board[row][col]) != number[i] or
                self.cover[row][col] != False):
                return None
        return True

    def strategies(self):
        #some explanations copied from http://www.minesweeper.info/wiki/Strategy
        #binomial coefficient taken from http://www.minesweeper.info/archive/MinesweeperStrategy/mine_probability_calculation_1.html
        return '''
        Reducing
        - Subtract the number of definite mines around a number 
            from the number on the board. Often, this reduces down
            to a pattern such as 121 or 1221.
        Common Patterns
        - 121: Mines must be on both sides of the 2.
        - 1221: 2 mines must be in the middle, with the 1's on the 
            edges both touching one mine.
        - 12: Whenever you see a 1-2 pattern 
            the 3rd square over is always a mine. 
        - 11: Whenever you see a 1-1 pattern starting from an 
            edge (or where an open square functions as an edge) 
            the 3rd square over is empty.
        Guessing Tips
        - Use the binomial coefficient n! / (k! * (n-k)!) where k = mines and n = squares
            to calculate probabilities. For more information, see
            http://www.minesweeper.info/archive/MinesweeperStrategy/mine_probability_calculation_1.html
        - If you can prove a square is safe, open it instead 
            of guessing where the mine is.
        - There might be an arrangement of numbers with more
            than one solution, and the solutions require different 
            amounts of mines. Instead of guessing, you can solve it by 
            flagging the rest of the board and seeing how many mines are left.
        - Sometimes it's better to guess randomly in the board than take a 50/50
             chance.
        - See http://nothings.org/games/minesweeper/ for more tips.
'''

    def redrawAll(self, canvas):
        #some from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        fontSize = int(self.cellWidth//3)
        #draw the teacher
        canvas.create_text(self.width - self.teacherWidth//2, self.height//20, 
        text = 'Teacher', font = 'Arial 30 bold')
        leftEdge = self.width-self.teacherWidth + self.margin
        topEdge = self.height//10
        bottomEdge = self.height - self.margin
        rightEdge = self.width - self.margin
        canvas.create_rectangle(leftEdge, topEdge, rightEdge, bottomEdge, width = 3)
        canvas.create_text(self.width - self.teacherWidth//2, self.height//3.5, 
        text = 
'''
press "p"
for probabilities
click on a board number
for a probability
explanation
press "s" for strategies
''', font = 'Arial 20 bold')
        #go through everything in the board
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = Game.getCellBounds(self, row, col)
                place = self.board[row][col]
                #if there's a mine, make the space red
                fill = "red" if place == '*' else "white"
                canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
                #mark numbers based on the number of mines around it
                if place != 0 and place != '*':
                    canvas.create_text(x0 + self.cellWidth//2, y0 + self.cellHeight//2, 
                    text = place, font = 'Arial ' + str(fontSize) + ' bold')
                #make cover
                if self.cover[row][col]:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='grey')
                #make flags
                if self.cover[row][col] == 'flag':
                    canvas.create_oval(x0, y0, x1, y1, fill='red')
                #if you flagged a square that isn't a mine, draw an X
                if self.cover[row][col] == 'wrong':
                    canvas.create_oval(x0, y0, x1, y1, fill='red')
                    canvas.create_line(x0, y0, x1, y1, width = 3)
                    canvas.create_line(x1, y0, x0, y1, width = 3)
                #draw probabilities
                if (self.AIScroll and self.cover[row][col]) or (self.getProbabilities and self.probabilities[row][col] != None and self.cover[row][col]):
                    canvas.create_text(x0 + self.cellWidth//2, y0 + self.cellHeight//2, 
                    text = self.probabilities[row][col], fill = 'yellow', font = 'Arial ' + str(fontSize) + ' bold')
                if self.AIScroll and self.moves != []:
                    if self.moves[self.movePlace][row][col]:
                        canvas.create_rectangle(x0, y0, x1, y1, fill='grey')
        
        if self.lost:
            canvas.create_text(self.width//2, self.height//2, 
                    text = 'YOU LOSE', font = 'Arial 75 bold')
            if self.AIScroll == False:
                canvas.create_rectangle(self.width - self.teacherWidth + self.margin*2, self.height//8, 
                    self.width - self.margin*2, self.height//5)
                canvas.create_text(self.width - 0.5*self.teacherWidth, self.height//6, 
                        text = 'Run AI', font = 'Arial 20 bold')
        if self.won:
            canvas.create_text(self.width//2, self.height//2, 
                    text = 'YOU WIN', font = 'Arial 75 bold')
            if self.AIScroll == False:
                canvas.create_rectangle(self.width - self.teacherWidth + self.margin*2, self.height//8, 
                    self.width - self.margin*2, self.height//5)
                canvas.create_text(self.width - 0.5*self.teacherWidth, self.height//6, 
                        text = 'Run AI', font = 'Arial 20 bold')
        if self.firstClick:
            canvas.create_text(self.width-self.width//6, self.height//2,
                text = 
'''
Click to clear a square. 
Right click to flag a mine 
(red circle). 
Don't hit any mines!
Click to start.
Manually change rows, cols, 
and mines.
''',
                font = 'Arial 20 bold')
        
        if self.getStrategies:
            canvas.create_rectangle(0, 0, self.width, self.height, fill='white')
            strategies = Game.strategies(self)
            canvas.create_text(self.width//2, self.height//2, text = strategies,
            font = 'Arial 20 bold')
        if self.pattern != None:
            canvas.create_text(self.width - self.teacherWidth//2, self.height//1.5,
            text = self.pattern, font = 'Arial 20 bold')

class State(object):
    #class copied from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html
    def __eq__(self, other): return (other != None) and self.__dict__ == other.__dict__
    def __hash__(self): return hash(str(self.__dict__)) # hack but works even with lists
    def __repr__(self): return str(self.__dict__)

class BacktrackingPuzzleSolver(object):
    #entire class modified from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html
    def solve(self, checkConstraints=True, printReport=False):
        self.moves = [ ]
        self.states = set()
        # If checkConstraints is False, then do not check the backtracking
        # constraints as we go (so instead do an exhaustive search)
        self.checkConstraints = checkConstraints
        # Be sure to set self.startArgs and self.startState in __init__
        self.startTime = time.time()
        self.solutionState = self.solveFromState(self.startState)
        self.endTime = time.time()
        if (printReport): self.printReport()
        return (self.moves, self.solutions)

    def printReport(self):
        print()
        print('***********************************')
        argsStr = str(self.startArgs).replace(',)',')') # remove singleton comma
        print(f'Report for {self.__class__.__name__}{argsStr}')
        print('checkConstraints:', self.checkConstraints)
        print('Moves:', self.moves)
        print('Solution state: ', end='')
        if ('\n' in str(self.solutionState)): print()
        print(self.solutionState)
        print('------------')
        print('Total states:', len(self.states))
        print('Total moves: ', len(self.moves))
        millis = int((self.endTime - self.startTime)*1000)
        print('Total time:  ', millis, 'ms')
        print('***********************************')

    def solveFromState(self, state):
        if state in self.states:
            # we have already seen this state, so skip it
            return None
        self.states.add(state)
        if self.isSolutionState(state):
            self.solutions.append(state)
        for move in self.getLegalMoves(state):
            # 1. Apply the move
            childState = self.doMove(state, move)
            # 2. Verify the move satisfies the backtracking constraints
            #    (only proceed if so)
            if self.stateSatisfiesConstraints(childState):
                # 3. Add the move to our solution path (self.moves)
                self.moves.append(move)
                # 4. Try to recursively solve from this new state
                result = self.solveFromState(childState)
                # 5. If we solved it, then return the solution!
                if result != None:
                    return result
                # 6. Else we did not solve it, so backtrack and
                #    remove the move from the solution path (self.moves)
                self.moves.pop()

class TankState(State):
    def __init__(self, minePositions):
        self.minePositions = minePositions

    def getMinePositions(self):
        return self.minePositions

class TankSolver(BacktrackingPuzzleSolver):
    def __init__(self, borderTiles):
        self.borderTiles = borderTiles
        self.minePositions = copy.deepcopy(self.borderTiles)
        self.rows = len(self.borderTiles)
        self.startArgs = self.minePositions
        self.startState = TankState(self.minePositions)
        self.solutions = []

    @staticmethod
    def checkForMines(self, row, col, place):
        number = 0
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                checkRow = row+drow
                checkCol = col+dcol
                if (checkRow, checkCol) == (row, col):
                    continue
                if (0 <= checkRow < self.rows and 0 <= checkCol < len(place[checkRow]) and
                    place[checkRow][checkCol][2] == 'True'):
                    number += 1
        return number

    def stateSatisfiesConstraints(self, state):
        # return True if the state satisfies the solution constraints so far
        for row in range(self.rows):
            cols = len(state.minePositions[row])
            for col in range(cols):
                if type(state.minePositions[row][col][2]) == int and state.minePositions[row][col][2] > 0:
                    #if the tile is a mine number
                    mines = self.checkForMines(self, row, col, state.minePositions)
                    if mines > state.minePositions[row][col][2]:
                        #if the number of marked mines is less than or equal to the number on the tile, it's fine
                        return False
        return True

    def isSolutionState(self, state):
        # return True if the state is a solution
        for row in range(self.rows):
            cols = len(state.minePositions[row])
            for col in range(cols):
                if type(state.minePositions[row][col][2]) == int and state.minePositions[row][col][2] > 0:
                    if (self.checkForMines(self, row, col, state.minePositions) != state.minePositions[row][col][2]):
                        return False
        return True

    def getLegalMoves(self, state):
        # return a list of the legal moves from this state (but not
        # taking the solution constraints into account)
        #compiles a list of legal moves that the mine can be placed in
        moves = []
        for row in range(len(self.borderTiles)):
            cols = len(self.borderTiles[row])
            for col in range(cols):
                if self.borderTiles[row][col][2] == None and type(self.borderTiles[row][col]) != int:
                    moves.append((row, col))
        return moves

    def doMove(self, state, move):
        # return a new state that results from applying the given
        # move to the given state
        # places the mine in the new location and returns the new locations
        (row, col) = move
        newPositions = copy.deepcopy(state.minePositions)
        newPositions[row][col] = (newPositions[row][col][0], newPositions[row][col][1], 'True')
        return TankState(newPositions)


Game(width = 1000, height = 700)