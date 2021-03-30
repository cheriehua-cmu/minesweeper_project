import copy
from fractions import Fraction

#my 2 problems:
#1 my definite probability functions are based on whether self.probabilities of that tile is None
#2 since my board takes in tiles based on unknowns, the probability distribution is inaccurate
#as I base the coordinates based on one start coordinate

L = [[(1, 0, 3), (1, 1, 2)], [(1, 2, 1)]]
print(L[0][0][2])



'''
#and i loop
            partialProbabilities = copy.deepcopy(positions[0])
            #set every value in partialProbabilities to 0
            for row in range(rows):
                cols = len(partialProbabilities[row])
                for col in range(cols):
                    partialProbabilities[row][col] = 0
'''
#go through the 2D list and set values equal to board values or '*' or '?'
    # @staticmethod
    # def getSurroundingTiles(self, row, col, place):
    #     tiles = []
    #     cols = len(place[row])
    #     for drow in [-1, 0, 1]:
    #         for dcol in [-1, 0, 1]:
    #             checkRow = row+drow
    #             checkCol = col+dcol
    #             if (0 <= checkRow < self.rows and 0 <= checkCol < len(place[checkRow]) and
    #                 type(place[checkRow][checkCol]) != int and (checkRow, checkCol) not in tiles):
    #                 tiles.append((checkRow, checkCol))
    #     return tiles

'''
        partialBoard = []
        rowList = []
        #go through everything in particalCoords and make it a 2D List
        for coords in partialCoords)):
            if coords > 0 and partialCoords[coords][0] != partialCoords[coords-1][0]:
                partialBoard.append(rowList)
                rowList = []
                rowList.append(partialCoords[coords])
            else:
                rowList.append(partialCoords[coords])
        partialBoard.append(rowList)
        print(partialBoard)
'''

'''
        rows = len(partialBoard)
        for row in range(rows):
            cols = len(partialBoard[row])
            for col in range(cols):
                r, c = partialBoard[row][col][0], partialBoard[row][col][1]
                if self.cover[r][c] == False:
                    partialBoard[row][col] = self.board[r][c]
                elif self.probabilities[r][c] == 1:
                    partialBoard[row][col] = '*'
                elif self.probabilities[r][c] == 0:
                    partialBoard[row][col] = '-'
                elif self.probabilities != 1:
                    partialBoard[row][col] = '?'


        if partialCoords != []:
            (startRow, startCol) = partialCoords[0]
'''
########################
#Name: Cherie Hua
#AndrewID: cxhua
#Section: O
# copied (with modifications) from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
#######################
import sys, math, copy, string, random, time
from cmu_112_graphics import * 
from fractions import Fraction #from https://docs.python.org/3.1/library/fractions.html
from tkinter import *
from PIL import Image

##############################################
# Generic backtracking-based puzzle solver
#
# Subclass this class to solve your puzzle
# using backtracking.
#
# To see how useful backtracking is, run with checkConstraints=True
# and again with checkConstraints=False
# You will see the number of total states go up (probably by a lot).
##############################################

import copy, time

class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_text(mode.width//2, mode.height//2,
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
            font = 'Arial 30 bold')
        

    def mousePressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)


class HelpMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, text='This is the help screen!', font=font)
        canvas.create_text(mode.width/2, 250, text='(Insert helpful message here)', font=font)
        canvas.create_text(mode.width/2, 350, text='Press any key to return to the game!', font=font)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 50

class GameMode(Mode):
    #will separate these functions later
    def appStarted(mode):
        mode.beginner = (9, 9, 10)
        mode.intermediate = (16, 16, 40)
        mode.expert = (16, 30, 99)
        mode.custom = ()
        mode.rows = 4
        mode.cols = 4
        mode.mines = 0
        mode.margin = mode.height//25
        mode.teacherWidth = mode.width//3
        mode.instructionsHeight = mode.height // 7
        mode.gridWidth  = mode.width - 2*mode.margin - mode.teacherWidth
        mode.gridHeight = mode.height - 2*mode.margin - mode.instructionsHeight
        mode.cellWidth  = mode.gridWidth // mode.cols
        mode.cellHeight = mode.gridHeight // mode.rows
        #creates base board
        mode.board = [[0, '*', 0, '*'], [0, 0, 0, 0], [0, 0, 0, 0], [0, '*', '*', 0]]
        #mode.board = [([0] * mode.cols) for row in range(mode.rows)]
        #creates a cover that the player can click to uncover
        mode.cover = [([True] * mode.cols) for row in range(mode.rows)]
        mode.lost = False
        mode.won = False
        mode.canClick = True
        mode.firstClick = True
        mode.probabilities = [([None] * mode.cols) for row in range(mode.rows)]
        mode.getProbabilities = True
        mode.reducedProbabilities = copy.deepcopy(mode.probabilities)
        mode.moves = []
        mode.moves.append(copy.deepcopy(mode.cover))
        mode.AIScroll = False
        mode.movePlace = 0
        mode.endScreen = None

    def generateMines(mode):
        #generates mines randomly until the number of mines generated equals the number
        #the player requested
        numMines = 0
        while numMines < mode.mines:
            row = random.randint(0, mode.rows)-1
            col = random.randint(0, mode.cols)-1
            if mode.board[row][col] != '*' and mode.board[row][col] != 'clear':
                mode.board[row][col] = '*'
                numMines += 1

    def placeNumbers(mode):
        #loop through every space in the board
        for row in range(mode.rows):
            for col in range(mode.cols):
                #if the space has a mine
                if mode.board[row][col] == 'clear':
                    mode.board[row][col] = 0
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.board[row][col] == '*':
                    #add 1 to the numbers around the mine
                    for drow in [-1, 0, 1]:
                        for dcol in [-1, 0, 1]:
                            if (drow, dcol) == (0, 0):
                                continue
                            checkRow = row+drow
                            checkCol = col+dcol
                            if (checkRow < mode.rows and checkCol < mode.cols 
                                and checkRow >= 0 and checkCol >= 0 and 
                                mode.board[checkRow][checkCol] != '*'):
                                mode.board[checkRow][checkCol] += 1

    def mousePressed(mode, event):
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        (row, col) = mode.getCell(event.x, event.y)
        if (row, col) != (-1, -1) and mode.canClick:
            if mode.firstClick:
                mode.firstClickF(row, col)
            if mode.cover[row][col] == 'flag':
                return
            if mode.cover[row][col] != 'flag':
                mode.cover[row][col] = False
            if (mode.cover[row][col] == False and mode.board[row][col] != '*' 
                and mode.board[row][col] > 0):
                mode.clearWithNumberPress(row, col)
            if mode.board[row][col] == '*' and mode.cover[row][col] != 'flag':
                mode.revealMines()
                mode.lost = True
                mode.canClick = False
            # if mode.getProbabilities and mode.probabilities[row][col]!= None:
            #     mode.getExplanation(mode, row, col)
            mode.expand(row, col)

    def clearWithNumberPress(mode, row, col):
        if mode.checkAround(row, col, 'flag', mode.cover) == mode.board[row][col]:
            for drow in [-1, 0, 1]:
                for dcol in [-1, 0, 1]:
                    if (drow, dcol) == (0, 0):
                        continue
                    checkRow = row+drow
                    checkCol = col+dcol
                    if (checkRow < mode.rows and checkCol < mode.cols 
                        and checkRow >= 0 and checkCol >= 0 and 
                        mode.cover[checkRow][checkCol] != 'flag'):
                            mode.cover[checkRow][checkCol] = False
                            if mode.board[checkRow][checkCol] == '*':
                                mode.revealMines()
                                mode.lost = True
                                mode.canClick = False

    def checkAround(mode, row, col, thing, place):
        number = 0
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if (drow, dcol) == (0, 0):
                    continue
                checkRow = row+drow
                checkCol = col+dcol
                if (checkRow < mode.rows and checkCol < mode.cols 
                    and checkRow >= 0 and checkCol >= 0 and place[checkRow][checkCol] == thing
                    and (drow, dcol) != (0, 0)):
                    number += 1
        return number

    def firstClickF(mode, row, col):
        #clears a larger then 1 block space on the first click
        mode.firstClick = False
        #clear a square no matter what the dimensions are
        rowOrCol = min(mode.rows, mode.cols)
        clearRows = rowOrCol//6 + 1
        clearCols = rowOrCol//6 + 1
        for clearRow in range(row-clearRows, row+clearRows):
            for clearCol in range(col-clearCols, col+clearCols):
                if (clearRow < mode.rows and clearCol < mode.cols 
                    and clearRow >= 0 and clearCol >= 0):
                    mode.board[clearRow][clearCol] = 'clear'
        mode.generateMines()
        mode.placeNumbers()

    def expand(mode, r, c):
        mode.cover[r][c] = False
        allClear = False
        while allClear == False:
            clearSpaces = 0
            for row in range(mode.rows):
                for col in range(mode.cols):
                    if mode.board[row][col] == 0 and mode.cover[row][col] == False:
                        for drow in [-1, 0, 1]:
                            for dcol in [-1, 0, 1]:
                                if (drow, dcol) == (0, 0):
                                    continue
                                checkRow = row+drow
                                checkCol = col+dcol
                                if (checkRow < mode.rows and checkCol < mode.cols 
                                    and checkRow >= 0 and checkCol >= 0):
                                    if (mode.board[checkRow][checkCol] != '*' and 
                                        mode.cover[checkRow][checkCol] == True):
                                        mode.cover[checkRow][checkCol] = False
                                        clearSpaces += 1
            if clearSpaces == 0:
                allClear = True

    def rightMousePressed(mode, event):
        #edited cmu_112_graphics.py to include right clicking, bounded to <Button-2>
        #from what I've seen online, right clicking is usually Button 3, and only Button 2 for OS X
        #so it may not work for non-Mac users
        (row, col) = mode.getCell(event.x, event.y)
        if mode.cover[row][col] != 'flag' and mode.canClick and mode.cover[row][col]:
            mode.cover[row][col] = 'flag'
        elif mode.cover[row][col] == 'flag' and mode.canClick:
            mode.cover[row][col] = True

    def getCellBounds(mode, row, col):
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        columnWidth = mode.gridWidth // mode.cols
        rowHeight = mode.gridHeight // mode.rows
        x0 = mode.margin + col * columnWidth
        x1 = mode.margin + (col+1) * columnWidth
        y0 = mode.margin + mode.instructionsHeight + row * rowHeight
        y1 = mode.margin + mode.instructionsHeight + (row+1) * rowHeight
        return (x0, y0, x1, y1)

    def pointInGrid(mode, x, y):
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        return ((mode.margin <= x <= mode.width-mode.margin-mode.teacherWidth) and
                (mode.margin + mode.instructionsHeight <= y <= mode.height-mode.margin))
    
    def getCell(mode, x, y):
        #from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        if not mode.pointInGrid(x, y):
            return (-1, -1)
        row = int((y - mode.margin - mode.instructionsHeight) // mode.cellHeight)
        col = int((x - mode.margin) // mode.cellWidth)
        return (row, col)

    def win(mode):
        #if every non-mine space is cleared, then set win to True and stop the player
        #from playing any more
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.board[row][col] != '*' and mode.cover[row][col] == True:
                    return False
        mode.revealMines()
        mode.canClick = False
        mode.won = True
        return True

    def revealMines(mode):
        #remove cover when the board has a mine
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.board[row][col] == '*' and mode.cover[row][col] != 'flag':
                    mode.cover[row][col] = False
                if mode.cover[row][col] == 'flag' and mode.board[row][col] != '*':
                    mode.cover[row][col] = 'wrong'

    def timerFired(mode):
        mode.win()
        mode.placeProbabilities()

    def tankSolver(mode, partialBoard):
        #print('tanksolver called')
        (move, solution) = TankSolver(partialBoard).solve()
        solutions = []
        if solution != None:
            for i in range(len(solution)):
                solutions.append(solution[i].minePositions)
            #print('solutions', solutions)
            return solutions

    def keyPressed(mode, event):
        #go to next move
        if mode.AIScroll:
            if event.key == 'Right' and mode.won == False and mode.lost == False:
                mode.executeMove(mode)
                #print("cover", mode.cover)
                if mode.cover not in mode.moves:
                    mode.moves.append(copy.deepcopy(mode.cover))
                mode.movePlace += 1
                if mode.movePlace >= len(mode.moves):
                    return
                if mode.endScreen != None and mode.movePlace == mode.endScreen[0]:
                        if mode.endScreen[1] == 'lost':
                            mode.lost = True
                        if mode.endScreen[1] == 'won':
                            mode.won = True
                #print("12345", len(mode.moves), mode.movePlace)
            if event.key == 'Left' and mode.movePlace > 0:
                if mode.lost:
                    mode.lost = False
                    mode.endScreen = (mode.movePlace, 'lost')
                if mode.won:
                    mode.won = False
                    mode.endScreen = (mode.movePlace, 'won')
                mode.movePlace -= 1
            #print('moves', mode.moves)
            #print('currentMove', mode.cover)

    def findMove(mode):
        if mode.firstClick:
            mode.firstClick = False
            #print('runs here')
            mode.firstClickF(mode.rows//2, mode.cols//2)
            return (mode.rows//2, mode.cols//2)

        probs = copy.deepcopy(mode.probabilities)
        #print('probs', probs)
        for r in range(mode.rows):
            for c in range(mode.cols):
                if probs[r][c] == None or mode.cover[r][c] == False:
                    probs[r][c] = 2

        minProb = min([min(value) for value in probs])
        
        #print('probabilities', probs)
        #print('minProb', minProb)
        for row in range(mode.rows):
            for col in range(mode.cols):
                if probs[row][col] == minProb:
                    (minRow, minCol) = (row, col)
        return (minRow, minCol)

    def executeMove(mode):
        if mode.won == False and mode.lost == False:
            (row, col) = mode.findMove(mode)
            mode.cover[row][col] = False
            mode.expand(row, col)
            #print(mode.cover)
            if mode.board[row][col] == '*':
                mode.lost = True
            win = True
            for row in range(mode.rows):
                for col in range(mode.cols):
                    if mode.cover[row][col] == True and mode.board[row][col] != '*':
                        win = False
            if win:
                mode.won = True

    def placeProbabilities(mode):
        #look through every tile
        for row in range(mode.rows):
            for col in range(mode.cols):
                #if there's a revealed number
                if (type(mode.board[row][col]) == int and mode.board[row][col] > 0 
                    and mode.cover[row][col] != True):
                    nUnrevealedTiles = mode.findUnrevealedTiles(row, col)
                    #place 1 if the number of tiles equals the number of mines
                    if nUnrevealedTiles == mode.board[row][col]:
                        #print('ran 1', row, col)
                        mode.definiteZerosAndOnes(row, col, 1)
                    #place 0 for the rest of the tiles in the area surrounding the number
                    nUnrevealedTiles = mode.findUnrevealedTiles(row, col)
                    #probabilitiesSum = mode.probabilitiesSum(mode, row, col)
                    nRevealedMines = mode.checkAround(row, col, 1, mode.probabilities)
                    if nRevealedMines == mode.board[row][col] and nRevealedMines < nUnrevealedTiles:
                        mode.definiteZerosAndOnes(row, col, 0)
                        #print('ran 0', row, col)
                        #print(probabilitiesSum)
        partialBoard = mode.getPartialBoard()
        if partialBoard != None:
            (rowStart, colStart) = partialBoard[0]
            borderTiles = copy.deepcopy(partialBoard)[1:]
            positions = mode.tankSolver(borderTiles)
            mode.getAIProbabilities(positions, rowStart, colStart)

    def getAIProbabilities(mode, positions, rowStart, colStart):
        if positions == []:
            return
        rows = len(positions[0])

        if len(positions) == 1:
            for state in positions:
                for row in range(rows):
                    cols = len(state[row])
                    for col in range(cols):
                        if row+rowStart < mode.rows and col+colStart < mode.cols:
                            if state[row][col] == '*':
                                mode.probabilities[row+rowStart][col+colStart] = 1
                            elif state[row][col] == '?':
                                mode.probabilities[row+rowStart][col+colStart] = 0
        else:
            #and i loop
            partialProbabilities = copy.deepcopy(positions[0])
            #set every value in partialProbabilities to 0
            for row in range(rows):
                cols = len(partialProbabilities[row])
                for col in range(cols):
                    partialProbabilities[row][col] = 0

            #add 1 to partialProbabilities if there's a mine in that location for each state
            for state in positions:
                for row in range(rows):
                    cols = len(state[row])
                    for col in range(cols):
                        if state[row][col] == '*':
                            partialProbabilities[row][col] += 1

            for row in range(rows):
                cols = len(partialProbabilities[row])
                for col in range(cols):
                    r = row+rowStart
                    c = col+colStart
                    if r < mode.rows and c < mode.cols and r >= 0 and c >= 0:
                        mode.probabilities[r][c] = Fraction(partialProbabilities[row][col], len(positions))

    def getPartialBoard(mode):
        partialCoords = []
        #go through everything in board
        for row in range(mode.rows):
            for col in range(mode.cols):
                #if it's a revealed number
                if mode.cover[row][col] == False:
                    #add it to partialCoords
                    partialCoords.append((row, col))
                    #add everything around it to partialCoords too if it's a covered tile
                    for drow in [-1, 0, 1]:
                        for dcol in [-1, 0, 1]:
                            if((drow,dcol) == (0,0)):
                                continue
                            checkRow = row+drow
                            checkCol = col+dcol
                            if (checkRow < mode.rows and checkCol < mode.cols 
                                and checkRow >= 0 and checkCol >= 0 
                                and mode.cover[checkRow][checkCol] != False
                                and (checkRow, checkCol) not in partialCoords):
                                partialCoords.append((checkRow, checkCol))
       
        partialCoords.sort(key = lambda tup: (tup[0], tup[1]))
        if partialCoords != []:
            (startRow, startCol) = partialCoords[0]
        
        partialBoard = []
        rowList = []
        #go through everything in particalCoords and make it a 2D List
        for coords in range(len(partialCoords)):
            if partialCoords[coords][0] != partialCoords[coords-1][0]:
                partialBoard.append(rowList)
                rowList = []
                rowList.append(partialCoords[coords])
            else:
                rowList.append(partialCoords[coords])
        partialBoard.append(rowList)


        #go through the 2D list and set values equal to board values or '*' or '?'
        rows = len(partialBoard)
        for row in range(rows):
            cols = len(partialBoard[row])
            for col in range(cols):
                r, c = partialBoard[row][col][0], partialBoard[row][col][1]
                if mode.cover[r][c] == False:
                    partialBoard[row][col] = mode.board[r][c]
                elif mode.probabilities[r][c] == 1:
                    partialBoard[row][col] = '*'
                elif mode.probabilities[r][c] != 1:
                    partialBoard[row][col] = '?'
        if partialCoords != []:
            return [(startRow, startCol)] + partialBoard

    def definiteZerosAndOnes(mode, row, col, thing):
        #place around the 8 squares around the number
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if (drow, dcol) == (0, 0):
                    continue
                checkRow = row+drow
                checkCol = col+dcol
                if (checkRow < mode.rows and checkCol < mode.cols 
                    and checkRow >= 0 and checkCol >= 0 and 
                    mode.cover[checkRow][checkCol] and mode.probabilities[checkRow][checkCol] != (1-thing)):
                        mode.probabilities[checkRow][checkCol] = thing

    def findUnrevealedTiles(mode, row, col):
        #count the number of covered tiles in the 8 squares surrounding a number
        nUnrevealedTiles = 0
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if (drow, dcol) == (0, 0):
                    continue
                checkRow = row+drow
                checkCol = col+dcol
                if (checkRow < mode.rows and checkCol < mode.cols
                    and checkRow >= 0 and checkCol >= 0 and mode.cover[checkRow][checkCol] != False
                    and mode.probabilities[checkRow][checkCol] != 0):
                    nUnrevealedTiles += 1
        return nUnrevealedTiles

    def getExplanation(mode, row, col):
        #explanations copied from http://www.minesweeper.info/wiki/Strategy
        basicRule = '''
If a number is touching the same 
number of squares, then the squares are all mines.
'''
        pattern121 = '''
Common pattern (121) - This is a variation of the 1-2 pattern.
There is 1 mine in the 
first two squares, and 2 mines in the 
first three squares. The 3rd square over 
must be a mine. Apply this from the other 
direction as well.'''
        pattern1221 = '''
Common pattern (1221) - This is a variation of the 1-2 pattern.
There is 1 mine in the 
first two squares, and 2 mines in the 
first three squares. The 3rd square over 
must be a mine. Apply this from the other 
direction as well.
'''
        pattern11 = '''
There is 1 mine in the first two squares, and 1 mine in the 
first three squares. The 3rd square over must be empty.
'''
        pattern12 = '''
There is 1 mine in the first two squares, and 2 mines in the 
first three squares. The 3rd square over must be a mine.
'''
        probability = '''
Of __ possible solutions, __ have a mine in this square.
        '''
        #if number > 121 or 1221 pattern, add 'Reduces to: '
    
    def strategies(mode):
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

    def redrawAll(mode, canvas):
        #some from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        fontSize = int(mode.cellWidth//2)
        #draw the teacher
        canvas.create_text(mode.width - mode.teacherWidth//2, mode.height//20, 
        text = 'Teacher', font = 'Arial 30 bold')
        leftEdge = mode.width-mode.teacherWidth + mode.margin
        topEdge = mode.height//10
        bottomEdge = mode.height - mode.margin
        rightEdge = mode.width - mode.margin
        canvas.create_rectangle(leftEdge, topEdge, rightEdge, bottomEdge, width = 3)
        #go through everything in the board
        for row in range(mode.rows):
            for col in range(mode.cols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                place = mode.board[row][col]
                #if there's a mine, make the space red
                fill = "red" if place == '*' else "white"
                canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
                #mark numbers based on the number of mines around it
                if place != 0 and place != '*':
                    canvas.create_text(x0 + mode.cellWidth//2, y0 + mode.cellHeight//2, 
                    text = place, font = 'Arial ' + str(fontSize) + ' bold')
                #make cover
                if mode.cover[row][col]:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='grey')
                #make flags
                if mode.cover[row][col] == 'flag':
                    canvas.create_oval(x0, y0, x1, y1, fill='red')
                #if you flagged a square that isn't a mine, draw an X
                if mode.cover[row][col] == 'wrong':
                    canvas.create_oval(x0, y0, x1, y1, fill='red')
                    canvas.create_line(x0, y0, x1, y1, width = 3)
                    canvas.create_line(x1, y0, x0, y1, width = 3)
                #draw probabilities
                #print(mode.probabilities)
                if (mode.AIScroll and mode.cover[row][col]) or (mode.getProbabilities and mode.probabilities[row][col] != None and mode.cover[row][col]):
                    canvas.create_text(x0 + mode.cellWidth//2, y0 + mode.cellHeight//2, 
                    text = mode.probabilities[row][col], fill = 'yellow', font = 'Arial ' + str(fontSize) + ' bold')
                if mode.AIScroll and mode.moves != []:
                    #print("fiuwdhbfiewubfioweubeu", mode.moves, mode.movePlace)
                    #print('bruh', mode.moves[mode.movePlace], row, col)
                    if mode.moves[mode.movePlace][row][col]:
                        canvas.create_rectangle(x0, y0, x1, y1, fill='grey')
        
        if mode.lost:
            canvas.create_text(mode.width//2, mode.height//2, 
                    text = 'YOU LOSE', font = 'Arial 75 bold')
            canvas.create_rectangle(mode.width - mode.teacherWidth + mode.margin*2, mode.height//8, 
                mode.width - mode.margin*2, mode.height//5)
            canvas.create_text(mode.width - 0.5*mode.teacherWidth, mode.height//6, 
                    text = 'Run AI', font = 'Arial 20 bold')
        if mode.won:
            canvas.create_text(mode.width//2, mode.height//2, 
                    text = 'YOU WIN', font = 'Arial 75 bold')
            canvas.create_rectangle(mode.width - mode.teacherWidth + mode.margin*2, mode.height//8, 
                mode.width - mode.margin*2, mode.height//5)
            canvas.create_text(mode.width - 0.5*mode.teacherWidth, mode.height//6, 
                    text = 'Run AI', font = 'Arial 20 bold')

class State(object):
    #class copied from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html
    def __eq__(mode, other): return (other != None) and mode.__dict__ == other.__dict__
    def __hash__(mode): return hash(str(mode.__dict__)) # hack but works even with lists
    def __repr__(mode): return str(mode.__dict__)

class BacktrackingPuzzleSolver(object):
    #entire class modified from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html
    def solve(mode, checkConstraints=True, printReport=False):
        mode.moves = [ ]
        mode.states = set()
        # If checkConstraints is False, then do not check the backtracking
        # constraints as we go (so instead do an exhaustive search)
        mode.checkConstraints = checkConstraints
        # Be sure to set mode.startArgs and mode.startState in __init__
        mode.startTime = time.time()
        mode.solutionState = mode.solveFromState(mode.startState)
        mode.endTime = time.time()
        if (printReport): mode.printReport()
        print('solutions in solver', mode.solutions)
        return (mode.moves, mode.solutions)

    def printReport(mode):
        print()
        print('***********************************')
        argsStr = str(mode.startArgs).replace(',)',')') # remove singleton comma
        print(f'Report for {mode.__class__.__name__}{argsStr}')
        print('checkConstraints:', mode.checkConstraints)
        print('Moves:', mode.moves)
        print('Solution state: ', end='')
        if ('\n' in str(mode.solutionState)): print()
        print(mode.solutionState)
        print('------------')
        print('Total states:', len(mode.states))
        print('Total moves: ', len(mode.moves))
        millis = int((mode.endTime - mode.startTime)*1000)
        print('Total time:  ', millis, 'ms')
        print('***********************************')

    def solveFromState(mode, state):
        if state in mode.states:
            # we have already seen this state, so skip it
            return
        mode.states.add(state)
        if mode.isSolutionState(state):
            mode.solutions.append(state)
            return
        for move in mode.getLegalMoves(state):
            # 1. Apply the move
            #print('move in template: ', move)
            childState = mode.doMove(state, move)
            # 2. Verify the move satisfies the backtracking constraints
            #    (only proceed if so)
            if mode.stateSatisfiesConstraints(childState):
                # 3. Add the move to our solution path (mode.moves)
                mode.moves.append(move)
                #print('moves after append', mode.moves)
                # 4. Try to recursively solve from this new state
                result = mode.solveFromState(childState)
                # 5. If we solved it, then return the solution!
                if result != None:
                    return result
                # 6. Else we did not solve it, so backtrack and
                #    remove the move from the solution path (mode.moves)
                #print('moves before pop', mode.moves)
                mode.moves.pop()

class TankState(State):
    def __init__(mode, minePositions):
        mode.minePositions = minePositions

    def getMinePositions(mode):
        #print('minePositions', mode.minePositions)
        return mode.minePositions

class TankSolver(BacktrackingPuzzleSolver):
    def __init__(mode, borderTiles):
        mode.borderTiles = borderTiles
        mode.minePositions = copy.deepcopy(mode.borderTiles)
        mode.rows = len(mode.borderTiles)
        mode.startArgs = mode.minePositions
        mode.startState = TankState(mode.minePositions)
        mode.solutions = []

    @staticmethod
    def splitBorderTiles(borderTiles):
        #will implement later...maybe
        pass

    @staticmethod
    def checkForMines(mode, row, col, place):
        number = 0
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if (drow, dcol) == (0, 0):
                    continue
                checkRow = row+drow
                checkCol = col+dcol
                if (0 <= checkRow < mode.rows and 0 <= checkCol < len(place[checkRow])
                    and place[checkRow][checkCol] == '*'):
                    number += 1
        return number


    def stateSatisfiesConstraints(mode, state):
        # return True if the state satisfies the solution constraints so far
        for row in range(mode.rows):
            cols = len(state.minePositions[row])
            for col in range(cols):
                if type(state.minePositions[row][col]) == int:
                    #if the tile is a mine number
                    #print('mines: ', (row, col), mode.checkForMines(mode, row, col, state.minePositions))
                    if mode.checkForMines(mode, row, col, state.minePositions) > state.minePositions[row][col]:
                        #if the number of marked mines is less than or equal to the number on the tile, it's fine
                        #print('fails to satisfy constraint', (row, col))
                        return False
        #print('satisfies constraint', (row, col))
        return True

    def isSolutionState(mode, state):
        # return True if the state is a solution
        for row in range(mode.rows):
            cols = len(state.minePositions[row])
            for col in range(cols):
                if type(state.minePositions[row][col]) == int:
                    if mode.checkForMines(mode, row, col, state.minePositions) != state.minePositions[row][col]:
                        #print('borderTiles', mode.borderTiles)
                        #print('not solution state', state.minePositions)
                        return False
        #print('mode.borderTiles', mode.borderTiles)
        #print('is solution state', state.minePositions)
        return True

    def getLegalMoves(mode, state):
        # return a list of the legal moves from this state (but not
        # taking the solution constraints into account)
        #compiles a list of legal moves that the mine can be placed in
        moves = []
        for row in range(len(mode.borderTiles)):
            cols = len(mode.borderTiles[row])
            for col in range(cols):
                if mode.borderTiles[row][col] == '?':
                    moves.append((row, col))
        return moves

    def doMove(mode, state, move):
        # return a new state that results from applying the given
        # move to the given state
        # places the mine in the new location and returns the new locations
        (row, col) = move
        newPositions = copy.deepcopy(state.minePositions)
        newPositions[row][col] = '*'
        #print('move', (row, col))
        return TankState(newPositions)


app = MyModalApp(width=1000, height=700)

'''
borderTiles = {(1, 1): [(1, 2), (1, 3), (1, 4)], (5, 5): [(5, 6), (5, 7), (5, 8)]}

moves = []
for key in borderTiles:
    for value in borderTiles[key]:
        moves.append(value)
print(moves)
'''

'''
L = [(0, 1), (1, 0), (0, 2)]
V = copy.deepcopy(L)[1:]
print()
'''

    # @staticmethod
    # def getSurroundingTiles(mode, row, col, place):
    #     tiles = []
    #     cols = len(place[row])
    #     for drow in [-1, 0, 1]:
    #         for dcol in [-1, 0, 1]:
    #             checkRow = row+drow
    #             checkCol = col+dcol
    #             if (0 <= checkRow < mode.rows and 0 <= checkCol < len(place[checkRow]) and
    #                 type(place[checkRow][checkCol]) != int and (checkRow, checkCol) not in tiles):
    #                 tiles.append((checkRow, checkCol))
    #     return tiles

'''
#finds tiles with most 0's -- if there's a fraction, that means there are no 0's... right?
    if self.firstClick:
        return (self.rows//2, self.cols//2)

    maxTilesRemoved = 0
    maxTile = (0, 0)
    for row in range(self.rows):
        for col in range(self.cols):
            if (type(self.board[row][col]) == int and self.cover[row][col] == False):
                surroundingTiles = Game.getSurroundingTiles(self, row, col)
                #surroundingTiles is a list of surrounding tiles
                tilesRemove = surroundingTiles.count(0)
                if tilesRemove > maxTilesRemoved:
                    maxTilesRemoved = tilesRemove
                    maxTile = (row, col)
    
    if maxTilesRemoved == 0:
        lowestProbability = 1
        for row in range(self.rows):
            for col in range(self.cols):
                if type(self.board[row][col]) == int and self.cover[row][col] == False:
                    lowProbability = Game.getLowProbability(self, row, col)
                    if lowProbability < lowestProbability:
                        lowestProbability = lowProbability
                        tile = (checkRow, checkCol)
    
    return tile

def getSurroundingTiles(self, row, col):
    tiles = []
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            checkRow = row+drow
            checkCol = col+dcol
            if (checkRow < self.rows and checkCol < self.cols
                and checkRow >= 0 and checkCol >= 0 and 
                self.cover[checkRow][checkCol] != False):
                tiles.append((checkRow, checkCol))
    return tiles
'''

L = [[1, 1, 2, 1], [3, 1, 2, 2]]
minProb = min([min(r) for r in L])
print()

'''
AI that solves the board

1. def findMove(self):
    minProb = min([min(r) for r in self.probabilities])
    for row in range(self.rows):
        for col in range(self.cols):
            if self.probabilities[row][col] == minProb:
                (minRow, minCol) = (row, col)
    return (minRow, minCol)

2. def executeMove(self):
    while self.won == False and self.lost == False:
        (row, col) = Game.findMove(self)
        self.cover[row][col] = False
        if self.board[row][col] == '*':
            self.lost = True
        win = True
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cover[row][col] == True and self.board[row][col] != '*':
                    win = False
        if win:
            self.won = True
        self.moves.append(self.cover)

3. def keyPressed(event)
    #go to next move
    if self.AIScroll:
        self.currentMove = self.moves[self.movePlace]


(if time, mayyyybeeee???) 6. def writeExplanations

'''

'''
explanations for certain patterns in sandbox mode

def getExplanations:
    ???

'''
'''
    def probabilitiesSum(self, row, col):
        pSum = 0
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if (drow, dcol) == (0, 0):
                    continue
                checkRow = row+drow
                checkCol = col+dcol
                if (checkRow < self.rows and checkCol < self.cols 
                    and checkRow >= 0 and checkCol >= 0 and 
                    self.cover[checkRow][checkCol] and 
                    self.probabilities[checkRow][checkCol] != None):
                    pSum += self.probabilities[checkRow][checkCol]
            return pSum
'''

#L = {(1, 2): [(1, 2), 2, 3], (2, 2): [0], (3, 2): [1], (4,2): [0]}
#for key in sorted(L):
#print(L[(1,2)][2])
##############################################
# Generic backtracking-based puzzle solver
#
# Subclass this class to solve your puzzle
# using backtracking.
#
# To see how useful backtracking is, run with checkConstraints=True
# and again with checkConstraints=False
# You will see the number of total states go up (probably by a lot).
##############################################

import copy, time

class BacktrackingPuzzleSolver(object):
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
        return (self.moves, self.solutionState)

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
            # we found a solution, so return it!
            return state
        else:
            for move in self.getLegalMoves(state):
                # 1. Apply the move
                childState = self.doMove(state, move)
                # 2. Verify the move satisfies the backtracking constraints
                #    (only proceed if so)
                if ((self.stateSatisfiesConstraints(childState)) or
                    (not self.checkConstraints)):
                    # 3. Add the move to our solution path (self.moves)
                    self.moves.append(move)
                    # 4. Try to recursively solve from this new state
                    result = self.solveFromState(childState)
                    # 5. If we solved it, then return the solution!
                    if result != None:
                        return result
                    # 6. Else we did not solve it, so backtrack and
                    #    remove the move from the solution path (self.moves)
                    print('before pop', self.moves)
                    self.moves.pop()
                    print('after pop', self.moves)
            return None

##############################################
# Generic State Class
#
# Subclass this with the state required by your problem.
# Note that this is a bit hacky with __eq__, __hash__, and __repr__
# (it's fine for 112, but after 112, you should take the time to
# write better class-specific versions of these)
##############################################

class State(object):
    def __eq__(self, other): return (other != None) and self.__dict__ == other.__dict__
    def __hash__(self): return hash(str(self.__dict__)) # hack but works even with lists
    def __repr__(self): return str(self.__dict__)
##############################################
# NQueensSolver and NQueensState
##############################################

class NQueensState(State):
    def __init__(self, n, queenPositions):
        self.n = n
        # queenPositions is a list of (row, col) positions of each queen
        self.queenPositions = queenPositions
    def __repr__(self):
        board = [ (['-'] * self.n) for row in range(self.n) ]
        for (row, col) in self.queenPositions:
            board[row][col] = 'Q'
        return '\n'.join([' '.join(row) for row in board])

class NQueensSolver(BacktrackingPuzzleSolver):
    def __init__(self, n):
        self.n = n
        self.startArgs = (n,) # for printReport
        self.startState = NQueensState(n, [ ])

    @staticmethod
    def queensAttackEachOther(row1, col1, row2, col2):
        return ((row1 == row2)               # same row
                or (col1 == col2)            # same col
                or (row1+col1 == row2+col2)  # same up-to-the-right diagonal
                or (row1-col1 == row2-col2)) # same down-to-the-right diagonal

    def stateSatisfiesConstraints(self, state):
        # The constraints are satisifed if no two queens can attack each other,
        # But we check this as we go, so we only have to check the last queen!
        (row1, col1) = state.queenPositions[-1] # this is the last queen added
        print(state.queenPositions)
        for (row2, col2) in state.queenPositions[:-1]:
            if (self.queensAttackEachOther(row1, col1, row2, col2)):
                return False
        return True

    def isSolutionState(self, state):
        if (len(state.queenPositions) < self.n):
            return False
        # Confirm that no two queens attack each other, but we have to check all
        # pairs of queens (since we can call solver with checkConstraints=False)
        for i in range(self.n):
            (row1, col1) = state.queenPositions[i]
            for j in range(i):
                (row2, col2) = state.queenPositions[j]
                if (self.queensAttackEachOther(row1, col1, row2, col2)):
                    return False
        return True

    def getLegalMoves(self, state):
        col = len(state.queenPositions)
        if (col == self.n):
            print([])
            return [ ]
        else:
            print([(row, col) for row in range(self.n)])
            return [(row, col) for row in range(self.n)]

    def doMove(self, state, move):
        newQueenPositions = state.queenPositions + [move]
        return NQueensState(self.n, newQueenPositions)

#NQueensSolver(7).solve(printReport=True)

'''
def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows = len(a)
    cols = len(a[0])
    fieldWidth = maxItemLength(a)
    print("[ ", end="")
    for row in range(rows):
        if (row > 0): print("\n  ", end="")
        print("[ ", end="")
        for col in range(cols):
            if (col > 0): print(", ", end="")
            # The next 2 lines print a[row][col] with the given fieldWidth
            formatSpec = "%" + str(fieldWidth) + "s"
            print(formatSpec % str(a[row][col]), end="")
        print(" ]", end="")
    print("]")

def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen


def reducedBoard(board, cover, probabilities):
        reducedBoard = copy.deepcopy(board)
        for row in range(rows):
            for col in range(cols):
                if probabilities[row][col] == 1:
                    for drow in [-1, 0, 1]:
                        for dcol in [-1, 0, 1]:
                            checkRow = row+drow
                            checkCol = col+dcol
                            if (checkRow < rows and checkCol < cols 
                                and checkRow >= 0 and checkCol >= 0):
                                print('pass 1')
                                if (type(reducedBoard[checkRow][checkCol]) == int and
                                reducedBoard[checkRow][checkCol] > 0):
                                    print('pass 2')
                                    if not cover[checkRow][checkCol]:
                                        print('pass 3')
                                        reducedBoard[checkRow][checkCol] -= 1
        print2dList(reducedBoard)
        return reducedBoard

board = [ [ 0, 0, 0, 1, '*', 1, 0, 0, 0, 0 ],
  [ 0, 0, 0, 1, 1, 2, 1, 2, 1, 1 ],
  [ 0, 0, 0, 0, 0, 1, '*', 2, '*', 1 ],
  [ 0, 0, 0, 0, 0, 1, 1, 2, 1, 1 ],
  [ 0, 0, 0, 0, 0, 0, 1, 1, 2, 1 ],
  [ 1, 1, 1, 0, 0, 0, 1, '*', 3, '*' ],
  [ 1, '*', 1, 0, 0, 0, 1, 1, 3, '*' ],
  [ 3, 3, 2, 0, 0, 1, 1, 1, 1, 1 ],
  [ '*', '*', 3, 2, 1, 2, '*', 2, 1, 1 ],
  [ '*', 4, '*', '*', 1, 2, '*', 2, 1, '*' ]]

rows = 10
cols = 10
cover = [[False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False]]
probabilities = [[None, None, None, None, 1, 0, 0, None, None, None], [None, None, None, None, None, None, 0, None, None, None], [None, None, None, None, None, None, 1, 0, None, None], [None, None, None, None, None, None, None, 0, None, None], [None, None, None, None, None, None, None, 0, None, None], [None, None, None, None, None, None, None, None, None, None], [0, 1, None, None, None, None, None, 0, None, None], [None, 0, None, None, None, None, None, 0, None, None], [None, None, None, None, None, None, 1, 0, None, None], [None, None, None, None, None, None, None, None, None, None]]


reducedBoard(board, rows, cols, cover, probabilities)
'''

'''
                    result = Game.isPattern(self, 121, row, col)
                    if result != None:
                        print(result)
                        (row121, col121, drow121, dcol121) = result
                        (tileRow, tileCol) = (0, 0)
                        for drow in [-1, +1]:
                            if self.cover[drow][col]:
                                tileRow = drow
                        for dcol in [-1, 1]:
                            if self.cover[row][dcol]:
                                tileCol = dcol
                        print(tileRow, tileCol)
                        row121 = row + tileRow
                        col121 = col + tileCol
                        if ((row121 + 2*drow121 >= 0) and (row121 + 2*drow121 < self.rows) and 
                            (col121 + 2*dcol121 >= 0) and (col121 + 2*dcol121 < self.cols)):
                            self.probabilities[row121][col121] = 1
                            self.probabilities[row121+drow121][col121+dcol121] = 0
                            self.probabilities[row121 + 2*drow121][col121 + 2*dcol121] = 1
                    if Game.is1221Pattern(self):
                        pass
'''
'''
    def isPattern(self, number, row, col):
        #modified from https://www.cs.cmu.edu/~112/notes/week5-case-studies.html#wordsearch1
        dcol = 0
        for drow in [-1, +1]:
            result = Game.isPatternHelper(self, number, row, col, drow, dcol)
            if (result != None):
                return result
        drow = 0
        for dcol in [-1, +1]:
            result = Game.isPatternHelper(self, number, row, col, drow, dcol)
            if (result != None):
                return result
        return None
    
    def isPatternHelper(self, number, startRow, startCol, drow, dcol):
        #modified from https://www.cs.cmu.edu/~112/notes/week5-case-studies.html#wordsearch1
        number = str(number)
        for i in range(len(number)):
            row = startRow + i*drow
            col = startCol + i*dcol
            if ((row < 0) or (row >= self.rows) or
                (col < 0) or (col >= self.cols) or
                (str(self.board[row][col]) != number[i]) or
                self.cover[row][col] != False):
                return None
        return (startRow, startCol, drow, dcol)

    def is1221Pattern(self):
        pass

    def reducedBoard(self, row, col, board):
        reducedBoard = copy.deepcopy(board)
        if self.probabilities[row][col] == 1:
            for drow in [-1, 0, 1]:
                for dcol in [-1, 0, 1]:
                    checkRow = row+drow
                    checkCol = col+dcol
                    if (checkRow < self.rows and checkCol < self.cols 
                        and checkRow >= 0 and checkCol >= 0 and 
                        type(reducedBoard[checkRow][checkCol]) == int and
                        reducedBoard[checkRow][checkCol] > 0 and 
                        self.cover[checkRow][checkCol]):
                        reducedBoard[checkRow][checkCol] -= 1
        return reducedBoard

#board = Game.reducedBoard(self, row, col, board)
                        #print(board)
'''
'''
                    zeroCount = Game.checkAround(self, row, col, 0, self.probabilities)
                    noneCount = Game.checkAround(self, row, col, None, self.probabilities)
                    if (nUnrevealedTiles - zeroCount == self.board[row][col] and nRevealedMines < nUnrevealedTiles):
                        print('RAN THIRD IF STATEMENT ', row, col)
                        print(zeroCount)
                        print(nUnrevealedTiles)
                        Game.definiteZerosAndOnes(self, row, col, 1)
'''
'''
        splitBorderTiles = []
        for thing in borderTiles:
            hasThing = False
            for value in borderTiles[thing]:
                for d in splitBorderTiles:
                    for v in splitBorderTiles[d]:
                        if value == v:
                            hasThing = True
                if hasThing == False:
                    newDict = dict()
                    newDict[thing] = borderTiles[thing]
            if len(newDict) != 0:
                splitBorderTiles.append(newDict)
        print(splitBorderTiles)
'''
'''
borderTiles[(row, col)] = Game.getUnknownTiles(self, row, col)
def getUnknownTiles(self, row, col):
    tiles = []
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            checkRow = row+drow
            checkCol = col+dcol
            if (checkRow < self.rows and checkCol < self.cols and 
                checkRow >= 0 and checkCol >= 0 and self.cover[checkRow][checkCol]
                and self.probabilities[checkRow][checkCol] != 1):
                    tiles.append((checkRow, checkCol))
    return tiles
'''
'''
partialBoard = []
for row in range(self.rows):
    rowList = []
    for col in range(self.cols):
        if (Game.checkAround(self, row, col, None, self.probabilities) > 
            Game.checkAround(self, row, col, False, self.cover) 
            and self.cover[row][col] == False):
            rowList.append((row, col))
            for drow in [-1, 0, 1]:
                for dcol in [-1, 0, 1]:
                    checkRow = row+drow
                    checkCol = col+dcol
                    if (checkRow < self.rows and checkCol < self.cols 
                        and checkRow >= 0 and checkCol >= 0 
                        and self.cover[checkRow][checkCol]
                        and self.probabilities[checkRow][checkCol] != 1
                        and (checkRow, checkCol) not in partialBoard
                        and (checkRow, checkCol) not in rowList):
                        rowList.append((checkRow, checkCol))
    partialBoard.append(rowList)
return partialBoard
'''