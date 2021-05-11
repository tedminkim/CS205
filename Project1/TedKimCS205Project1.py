from copy import deepcopy

#Global variables used for final calculated results
expandedTotal = 0
maxNodes = 0
goalDepth = 0
useQ = []

#Node class, for each node state in the state tree
class Node:
    def __init__(self, angelicaPuzzle, gn, hn):
        self.angelicaPuzzle = angelicaPuzzle #This is the "angelicaPuzzle", or the puzzle that is included in the node object (for the general search function initialization of the node)
        self.gn = gn #Path Cost, g(n)
        self.hn = hn #Heuristic Cost, h(n)
        self.fn = self.gn + self.hn #For A*, the value of f(n)
        self.goalState = [['A', 'N', 'G'], ['E', 'L', 'I'], ['C', 'A', '.']] #Goal State

#angelicaPuzzle class, for printing the puzzle, and the class also has a goal state attribute, which will be used to compare in order to see
#if the user successfully completed the Puzzle
class AngelicaPuzzle:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.goalState = [['A', 'N', 'G'], ['E', 'L', 'I'], ['C', 'A', '.']]

    #For the print functions, referenced these from Stack Overflow:
    #https://stackoverflow.com/questions/31232320/how-to-store-and-print-a-list-of-numbers-in-matrix-formpython
    #https://stackoverflow.com/questions/28205805/how-do-i-create-3x3-matrices
    def printEachArray(self, puzzle):
        print("\t" + " ".join(puzzle))

    def printPuzzle(self, puzzle):
        for i in puzzle:
            self.printEachArray([str(j) for j in i])

    def print(self):
        self.printPuzzle(self.puzzle)

#Calculating hn value for misplaced tile hn
def misplacedHeuristic(state):
    totalMisplaced = 0 #Count that will keep track of each misplaced tile found
    for i in range(3):
        for j in range(3):
            if state.angelicaPuzzle.puzzle[i][j] != state.angelicaPuzzle.goalState[i][j] and state.angelicaPuzzle.puzzle[i][j] != '.': #Comparing each individual tile to where it should be in the goal state
                totalMisplaced = totalMisplaced + 1 #Increment count variable if the tile is indeed misplaced.

    return totalMisplaced #Return the total number of misplaced tiles

#Calculating hn value for manhattan distance hn
def manhattanHeuristic(state):
    manhattanSum = 0 #Variable used to return the final manhattan distance heuristic value
    #If the location of each value on a puzzle was plotted on a coordinate, these variables are used as x and y coordinate values.
    x = 0
    y = 0
    for i in range(3):
        for j in range(3):
            if state.angelicaPuzzle.puzzle[i][j] != '.':#If the value of the matrix at this specific index is 0, the "blank", then we need to check for the following conditions
                if state.angelicaPuzzle.puzzle[i][j] == 'A':#If value is 1, calculate manhattan distance from correct place using appropriate index values for correct location
                    x = 0
                    y = 0
                elif state.angelicaPuzzle.puzzle[i][j] == 'N':#If value is 2, calculate manhattan distance from correct place using appropriate index values for correct location
                    x = 0
                    y = 1
                elif state.angelicaPuzzle.puzzle[i][j] == 'G':#If value is 3, calculate manhattan distance from correct place using appropriate index values for correct location
                    x = 0
                    y = 2
                elif state.angelicaPuzzle.puzzle[i][j] == 'E':#If value is 4, calculate manhattan distance from correct place using appropriate index values for correct location
                    x = 1
                    y = 0
                elif state.angelicaPuzzle.puzzle[i][j] == 'L':#If value is 5, calculate manhattan distance from correct place using appropriate index values for correct location
                    x = 1
                    y = 1
                elif state.angelicaPuzzle.puzzle[i][j] == 'I':#If value is 6, calculate manhattan distance from correct place using appropriate index values for correct location
                    x = 1
                    y = 2
                elif state.angelicaPuzzle.puzzle[i][j] == 'C':#If value is 7, calculate manhattan distance from correct place using appropriate index values for correct location
                    x = 2
                    y = 0
                elif state.angelicaPuzzle.puzzle[i][j] == 'A':#If value is 8, calculate manhattan distance from correct place using appropriate index values for correct location
                    x = 2
                    y = 1
                a = abs(i-x)
                b = abs(j-y)
                manhattanSum = manhattanSum + a + b #Totalling manhattan distance using a and b values from x and y.

    return manhattanSum

#Swap function that can be used to swap values (maybe to help with the operators)
def swap(a,b):
    temp = a
    a = b
    b = temp


#Operators to move the blank either left, right, up, or down.
def moveUp(parentNode, movingUp):
    #print("Going Up")
    canGoUp = True
    #keepTrack = []
    if '.' in parentNode.angelicaPuzzle.puzzle[0]:
        canGoUp = False
    if canGoUp:
        for i in parentNode.angelicaPuzzle.puzzle:
            if i.count('.') == 1 and i != movingUp.angelicaPuzzle.puzzle[0] and i == parentNode.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 2]: #Occurence of a list item https://www.w3schools.com/python/ref_list_count.asp
                movingUp.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 2][i.index('.')] = movingUp.angelicaPuzzle.puzzle[0][i.index('.')] #Position of list item https://www.w3schools.com/python/ref_list_index.asp
                movingUp.angelicaPuzzle.puzzle[0][i.index('.')] = '.'
                useQ.append(parentNode.angelicaPuzzle.puzzle)
            elif i.count('.') == 1 and i != movingUp.angelicaPuzzle.puzzle[0] and i == parentNode.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 1]:
                movingUp.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 1][i.index('.')] = movingUp.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 2][i.index('.')]
                movingUp.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 2][i.index('.')] = '.'
                useQ.append(parentNode.angelicaPuzzle.puzzle)


def moveDown(parentNode, movingDown):
    #print("Going Down")
    canGoDown = True
    #keepTrack = []
    if '.' in parentNode.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 1]:
        canGoDown = False
    if canGoDown:
        for i in parentNode.angelicaPuzzle.puzzle:
            if i.count('.') == 1 and i != parentNode.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 1] and i == parentNode.angelicaPuzzle.puzzle[0]: #Occurence of a list item https://www.w3schools.com/python/ref_list_count.asp
                movingDown.angelicaPuzzle.puzzle[0][i.index('.')] = movingDown.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 2][i.index('.')] #Position of list item https://www.w3schools.com/python/ref_list_index.asp
                movingDown.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 2][i.index('.')] = '.'
                useQ.append(parentNode.angelicaPuzzle.puzzle)
            elif i.count('.') == 1 and i != parentNode.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 1] and i == parentNode.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 2]:
                movingDown.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 2][i.index('.')] = movingDown.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 1][i.index('.')]
                movingDown.angelicaPuzzle.puzzle[len(parentNode.angelicaPuzzle.puzzle) - 1][i.index('.')] = '.'
                useQ.append(parentNode.angelicaPuzzle.puzzle)

def moveLeft(movingLeft, parentNode):
    #keepTrack = []
    #print("Going Left")
    #movingLeft = deepcopy(parentNode)
    canGoLeft = True
    blankTracker = 0
    for i in range(len(movingLeft.angelicaPuzzle.puzzle)):
        if movingLeft.angelicaPuzzle.puzzle[i][0] == '.':
            canGoLeft = False
    if canGoLeft:
        for i in movingLeft.angelicaPuzzle.puzzle: #Iterate through the puzzle that will be deep copied (in the expand() function)
            if i.count('.') == 1 and i.index('.') != '.': #Occurence of a list item https://www.w3schools.com/python/ref_list_count.asp, aka if there is only one occurence of 0, our blank
                blankTracker = i.index('.') ##Position of list item https://www.w3schools.com/python/ref_list_index.asp, aka if it is not located at the leftmost side of the puzzle; use to make it easier to replace
                i[blankTracker] = i[blankTracker - 1] #replacing the value
                i[blankTracker - 1] = '.' #new 0 position
                useQ.append(parentNode.angelicaPuzzle.puzzle)


def moveRight(movingRight, parentNode):
    #print("Going Right")
    #movingRight = deepcopy(parentNode)
    canGoRight = True
    blankTracker = 0
    for i in range(len(movingRight.angelicaPuzzle.puzzle)):
        if movingRight.angelicaPuzzle.puzzle[i][len(movingRight.angelicaPuzzle.puzzle) - 1] ==  '.':
            canGoRight = False
    if canGoRight:
        for i in movingRight.angelicaPuzzle.puzzle:
            if i.count('.') == 1 and i.index('.') != (len(parentNode.angelicaPuzzle.puzzle) - 1): #Occurence of a list item https://www.w3schools.com/python/ref_list_count.asp
                blankTracker = i.index('.')                 #Position of list item https://www.w3schools.com/python/ref_list_index.asp
                i[blankTracker] = i[blankTracker + 1]
                i[blankTracker + 1] = '.'
                useQ.append(parentNode.angelicaPuzzle.puzzle)


#deepcopy used from Python's copy library
#Link to Python 3.9.2 documentation: https://docs.python.org/3/contents.html
def expand(parentNode):
    global useQ

    gCost = str(parentNode.gn)  # Path cost g(n)
    hCost = str(parentNode.hn)  # Heuristic cost h(n)
    keepTrack = []
    bestStateStr = "The best state to expand with a g(n) = " + gCost + " and h(n) = " + hCost + " is...\n"
    print(bestStateStr)
    parentNode.angelicaPuzzle.print()
    print("Expanding this node...")



    movingUp = deepcopy(parentNode)
    movingDown = deepcopy(parentNode)
    movingLeft = deepcopy(parentNode)
    movingRight = deepcopy(parentNode)

    moveUp(parentNode, movingUp)
    keepTrack.append(movingUp)
    movingUp.gn = movingUp.gn + 1
    movingUp.fn = movingUp.gn + movingUp.hn

    moveDown(parentNode, movingDown)
    keepTrack.append(movingDown)
    movingDown.gn = movingDown.gn + 1
    movingDown.fn = movingDown.gn + movingDown.hn

    moveLeft(movingLeft,parentNode)
    keepTrack.append(movingLeft)
    movingLeft.gn = movingLeft.gn + 1
    movingLeft.fn = movingLeft.gn + movingLeft.hn

    moveRight(movingRight, parentNode)
    keepTrack.append(movingRight)
    movingRight.gn = movingRight.gn + 1
    movingRight.fn = movingRight.gn + movingRight.hn



    return keepTrack

"""
General (Generic) Search Algorithm:
function general-search(problem, QUEUEING-FUNCTION)
    nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
    loop do
        if EMPTY(nodes) then return "failure"
        node = REMOVE-FRONT(nodes)
        if problem.GOAL-TEST(node.STATE) succeeds then return node
        nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))

This is the algorithm being imitated / implemented into Python syntax.
"""
def generalSearch(problem, algorithmName):
    global maxNodes
    global goalDepth
    node = Node(problem, 0, 0) #The initial state of the puzzle
    nodes = [node] #MAKE-QUEUE, but in python using a queue of nodes
    while 1:
        if (len(nodes) > maxNodes):
            maxNodes = len(nodes)
        if len(nodes) == 0:
            print("No solution found.")
            return 0
        node = removeFront(nodes)
        if problem.goalState == node.angelicaPuzzle.puzzle:
            goalDepth = node.gn
            #print(goalDepth)
            expandedInStr = str(expandedTotal)
            maxInStr = str(maxNodes)
            goalInStr = str(goalDepth)
            # Print success message, with given values of totan number of expanded nodes, max number of nodes in the queue, and the depth of the goal in the state tree
            print("Solution found!")
            node.angelicaPuzzle.print()
            print("To solve this problem, the search algorithm expanded a total of: " + expandedInStr + " nodes.")
            print("The maximum number of nodes in the queue at any one time was: " + maxInStr + " nodes.")
            print("The depth of the goal node was: " + goalInStr + ".")
            return node
        nodes = queueingFunction(expand(node), algorithmName, nodes)

def removeFront(nodes):
    #Lambda sort method acquired from the following stack overflow link:
    #https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
    nodes.sort(key=lambda nodes: nodes.fn, reverse=True)
    #for i in range(len(nodes)):
    #    print(nodes[i].fn)
    ye = nodes[0]
    index = 0
    for i in range(len(nodes)):
        if nodes[i].fn < ye.fn:
            index = i
    ye = nodes[index]
    nodes.pop(index)
    return ye

def queueingFunction(node, algorithmName, nodes):
    global expandedTotal
    for i in node:
        if algorithmName == "UniformCostSearch":
            i.hn = 0
            if i.angelicaPuzzle.puzzle not in useQ:
                index = node.index(i)
                nodes.insert(index, i)
                useQ.append(i.angelicaPuzzle.puzzle)
                expandedTotal = expandedTotal + 1
        if algorithmName == "MisplacedTiles":
            i.hn = misplacedHeuristic(i)
            if i.angelicaPuzzle.puzzle not in useQ:
                nodes.append(i)
                useQ.append(i.angelicaPuzzle.puzzle)
                expandedTotal = expandedTotal + 1
        if algorithmName == "ManhattanDistance":
            i.hn = manhattanHeuristic(i)
            if i.angelicaPuzzle.puzzle not in useQ:
                nodes.append(i)
                useQ.append(i.angelicaPuzzle.puzzle)
                expandedTotal = expandedTotal + 1

    return nodes


def main():
    userInput = ""  # variable that will be used to receive user input
    userPuzzle = None  # Puzzle initialized to nothing
    defaultPuzzle = [['A', 'N', 'G'], ['E', 'L', 'I'], ['C', '.', 'A']]  # Puzzle that will be used as default puzzle with user enters 1
    print("Welcome to Ted Kim's Angelica Puzzle solver!")
    while userInput != "1" and userInput != "2":  # This while loop will continue if the user fails the input the correct input of either 1 or 2
        userInput = input("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle.")  # Prompts the user
        if userInput == "1":
            print("Default puzzle selected. Using default.")
            userPuzzle = AngelicaPuzzle(defaultPuzzle)  # Create angelicaPuzzle Object with the defaultPuzzle.
            userPuzzle.print()  # Print the puzzle
        elif userInput == "2":
            print("Enter your puzzle, use a zero to represent the blank")
            # Take the three rows of input, and put them in individual lists, eliminating the spaces/tabs in between each number
            row1 = input("Enter the first row, use space or tabs between letters: ")
            row1 = [str(s) for s in row1.split()]  # Code snippet found on StackOverflow: https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python
            row2 = input("Enter the second row, use space or tabs between letters: ")
            row2 = [str(s) for s in row2.split()]  # Code snippet found on StackOverflow: https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python
            row3 = input("Enter the third row, use space or tabs between letters: ")
            row3 = [str(s) for s in row3.split()]  # Code snippet found on StackOverflow: https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python

            userPuzzle = AngelicaPuzzle([row1, row2, row3])  # Creates angelicaPuzzle object using the three rows made from user's input
            userPuzzle.print()  # Print the puzzle

    chooseAlgorithm(userPuzzle)  # Transition to the user selecting which algorithm to solve the userPuzzle with.

def chooseAlgorithm(userPuzzle):
    userInput = ""
    algorithmName = ""
    node = None
    while userInput != '1' and userInput != '2' and userInput != '3': #Will not exit loop unless correct input is given
        print("Enter your choice of algorithm")
        print("1. Uniform Cost Search")
        print("2. A* with the Misplaced Tile Heuristic")
        print("3. A* with the Manhattan distance Heuristic")
        userInput = input()
        #Begin general search algorithm on the puzzle based on which number the user inputs as their algorithm method of choice
        if userInput == '1':
            algorithmName = "UniformCostSearch"
            print("Running Uniform Cost Search on")
            userPuzzle.print()
        elif userInput == '2':
            algorithmName = "MisplacedTiles"
            print("Running A* w/ Misplaced Tile Heuristic On")
            userPuzzle.print()
        elif userInput == '3':
            algorithmName = "ManhattanDistance"
            print("Running A* w/ Manhattan Distance Heuristic on")
            userPuzzle.print()

        node = generalSearch(userPuzzle, algorithmName) #Call the function on the userPuzzle, assigning the reuslt to node


main()
