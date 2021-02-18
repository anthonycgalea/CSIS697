def printGrid(grid, visited, showGrid):
    print("Grid Looks Like:")
    for k in range(len(grid)):
        s = " "
        if (showGrid == False):
            s=" ".join(grid[k])
        else:
            for l in range(len(grid[k])):
                if ([k, l] in visited and grid[k][l] == "."):
                    s+=" "
                else:
                    s+=grid[k][l]
                s+=" "
        print(s)

def displayMenu():
    print("L:\tTurn Left\nR:\tTurn Right\n[x]:\tMove x number of steps\nC:\tConsume Item\nP:\tPlace Item\nS:\tShow/Hide Path\nQ:\tQuit")

def turnLeft(currentChar):
    if (currentChar == "@"):
        return "@"
    elif (currentChar == "v"):
        return ">"
    elif(currentChar == ">"):
        return "^"
    elif(currentChar == "^"):
        return "<"
    else:
        return "v"

def turnRight(currentChar):
    if (currentChar == "@"):
        return "@"
    elif (currentChar == "v"):
        return "<"
    elif(currentChar == ">"):
        return "v"
    elif(currentChar == "^"):
        return ">"
    else:
        return "^"    

f = open("init_grid.txt")
showGrid = True
visited = []
num = f.readline().split(" ")
grid = [["." for k in range(int(num[1]))] for l in range(int(num[0]))]
initpos = f.readline().split(" ")
initdir = f.readline().strip()
dirchar = ""
if (initdir=='N'):
    dirchar = "^"
elif(initdir == 'S'):
    dirchar = "v"
elif(initdir == 'W'):
    dirchar = "<"
else:
    dirchar = ">"
grid[int(initpos[0])][int(initpos[1])] = dirchar
numObs = int(f.readline())
for k in range(numObs):
    obPos = f.readline().split(" ")
    grid[int(obPos[0])][int(obPos[1])] = "x"
numItems = int(f.readline())
for k in range(numItems):
    obPos = f.readline().split(" ")
    if (obPos[0] == initpos[0] and obPos[1] == initpos[1]):
       grid[int(obPos[0])][int(obPos[1])] = "@" 
    else:
        grid[int(obPos[0])][int(obPos[1])] = "o"
print("Finished reading initial grid from file.")
printGrid(grid, visited, showGrid)
print("-----Welcome to Pacman-----")
userInput = "default"
displayMenu()
currentPosY = int(initpos[0])
currentPosX = int(initpos[1])
currentDirection = grid[currentPosY][currentPosX] 
first = True
while(not userInput == "Q"):
    if (not first):
        printGrid(grid, visited, showGrid)
    first = False
    userInput=input(">")
    if (userInput=="Q" or userInput=="q"):
        print("Quitting...")
    elif(userInput=="L" or userInput=="l"):
        currentDirection = turnLeft(currentDirection)
        grid[currentPosY][currentPosX] = turnLeft(grid[currentPosY][currentPosX])
    elif(userInput=="R" or userInput=="r"):
        currentDirection = turnRight(currentDirection)
        grid[currentPosY][currentPosX] = turnRight(grid[currentPosY][currentPosX])
    elif(userInput=="C" or userInput=="c"):
        if (grid[currentPosY][currentPosX] == "@"):
            grid[currentPosY][currentPosX] = currentDirection
    elif(userInput=="P" or userInput=="p"):
        grid[currentPosY][currentPosX] = "@"
    elif(userInput=="S"):
        showGrid = not showGrid
    elif(userInput.isnumeric()):
        userInput = int(userInput)
        validMove = True
        newMoves = []
        #horizontal movement
        if (currentDirection == ">" or currentDirection == "<"):
            if (currentDirection == "<"):
                userInput*=-1
            if (not (currentPosX + userInput < 0 or currentPosX + userInput >= int(num[1]))):
                for k in range(currentPosX,currentPosX+userInput+int(userInput/abs(userInput)),int(userInput/abs(userInput))):
                    if (grid[currentPosY][k] == "x"):
                        validMove=False
                    newMoves.append([currentPosY, k])
                if (validMove):
                    for move in newMoves:
                        visited.append(move)
                    if (grid[currentPosY][currentPosX] == "@"):
                        grid[currentPosY][currentPosX] = "o"
                    else:
                        grid[currentPosY][currentPosX] = "."
                    currentPosX+=userInput
                    if (grid[currentPosY][currentPosX] == "o"):
                        grid[currentPosY][currentPosX] = "@"
                    else:
                        grid[currentPosY][currentPosX] = currentDirection
                else:
                    print("Invalid move. Enter again")
            else:
                print("Invalid move. Enter again")
        #vertical movement
        elif (currentDirection == "^" or currentDirection == "v"):
            if (currentDirection == "^"):
                userInput*=-1
            if (not (currentPosY + userInput < 0 or currentPosY + userInput >= int(num[0]))):
                for k in range(currentPosY,currentPosY+userInput+int(userInput/abs(userInput)),int(userInput/abs(userInput))):
                    if (grid[k][currentPosX] == "x"):
                        validMove=False
                    newMoves.append([k, currentPosX])
                if (validMove):
                    for move in newMoves:
                        visited.append(move)
                    if (grid[currentPosY][currentPosX] == "@"):
                        grid[currentPosY][currentPosX] = "o"
                    else:
                        grid[currentPosY][currentPosX] = "."
                    currentPosY+=userInput
                    if (grid[currentPosY][currentPosX] == "o"):
                        grid[currentPosY][currentPosX] = "@"
                    else:
                        grid[currentPosY][currentPosX] = currentDirection
                else:
                    print("Invalid move. Enter again")
            else:
                print("Invalid move. Enter again")
    else:
        print("Invalid input. Please try again.")