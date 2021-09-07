# --------- RULES FOR ALIVE CELLS ---------
# Less than Two Neighbours = die
# Two or Three Neighbours = stay alive
# More than Three Neighbours = die

# --------- RULES FOR EMPTY SPACES ---------
# Three Neighbours = born

# --------- CONTROLS ---------
# Space - Starts the game
# R - Resets the game board
# T - Reverts to board before game start
# Left Mouse - Places cells
# Right Mouse - Deletes Cells

import pygame
import math

pygame.font.init()
font = pygame.font.SysFont("Times New Roman, Arial", 25, bold=True)

# --------- Modification Variables ---------
rows, cols = 12, 12
cellSize = 30
runFPS = 10
menuFPS = 999
showGrid = True
showStats = True

FPS = menuFPS
fpsClock = pygame.time.Clock()

window = pygame.display.set_mode( (cols * cellSize, rows * cellSize) )
pygame.display.set_caption("Conway's Game of Life")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

grid = []
prevGrid = None
removedCells = [] # Cells to be removed in the next frame
bornCells = [] # Cells to be born in the next frame

# Statistics
numGenerations = 0
numCellsAlive = 0

def getNumCellsAlive():

    count = 0

    for row in range(grid.__len__()):
        for col in range(grid[row].__len__()):
            if grid[row][col]:
                count += 1

    return count

def draw():

    global numCellsAlive

    # Draw Stuff
    window.fill(BLACK)

    # Draw Cells
    for row in range(grid.__len__()):
        for col in range(grid[row].__len__()):
            if grid[row][col]:
                pygame.draw.rect(window, WHITE, (col * cellSize, row * cellSize, cellSize, cellSize))
            else:
                pygame.draw.rect(window, BLACK, (col * cellSize, row * cellSize, cellSize, cellSize))

    # Draw Grid
    if showGrid:
        for i in range(rows):
            pygame.draw.line(window, GRAY, (0, i * cellSize), (cols * cellSize, i * cellSize))
        for i in range(cols):
            pygame.draw.line(window, GRAY, (i * cellSize, 0), (i * cellSize, rows * cellSize))

    # Statistics
    if showStats:

        genText = font.render("Generations: " + str(numGenerations), True, RED)
        cellsAliveText = font.render("Cells Alive: " + str(numCellsAlive), True, RED)
        window.blit(genText, (15, 5))
        window.blit(cellsAliveText, (15, 45))

    numCellsAlive = getNumCellsAlive()

    # Update Display
    pygame.display.update()

def mouseAction(adding):

    global grid

    mx, my = pygame.mouse.get_pos()
    mousePos = [math.floor(mx / cellSize), math.floor(my / cellSize)]

    if adding:
         grid[mousePos[1]][mousePos[0]] = True
    else:
         grid[mousePos[1]][mousePos[0]] = False

def getNumAdjacentCells(row, col):

    count = 0

    if row > 0:

        if grid[row - 1][col]:
            count += 1

        if col > 0 and grid[row - 1][col - 1]:
            count += 1

        if col < cols - 1 and grid[row - 1][col + 1]:
            count += 1

    if row < rows - 1:

        if grid[row + 1][col]:
            count += 1

        if col > 0 and grid[row + 1][col - 1]:
            count += 1

        if col < cols - 1 and grid[row + 1][col + 1]:
            count += 1

    if col > 0 and grid[row][col - 1]:
        count += 1

    if col < cols - 1 and grid[row][col + 1]:
        count += 1

    return count

def updateGrid():

    global grid
    global numGenerations

    for row in range(grid.__len__()):
        for col in range(grid[row].__len__()):

            numAdjacent = getNumAdjacentCells(row, col)

            if (numAdjacent < 2 or numAdjacent > 3) and grid[row][col]:
                removedCells.append([row, col])

            elif numAdjacent == 3 and not grid[row][col]:
                bornCells.append([row, col])

    for i in removedCells:
        grid[i[0]][i[1]] = False

    for i in bornCells:
        grid[i[0]][i[1]] = True

    removedCells.clear()
    bornCells.clear()

    numGenerations += 1

def restart():

    global removedCells, bornCells, numGenerations, numCellsAlive, FPS

    removedCells.clear()
    bornCells.clear()
    FPS = menuFPS
    numGenerations = 0
    numCellsAlive = 0

def main():

    global grid
    global FPS
    global prevGrid

    grid = [ [False] * cols for i in range(rows) ]
    run = True
    start = False

    # Game Loop
    while run:

        fpsClock.tick(FPS)

        # Check Events
        for event in pygame.event.get():

            # User exits window
            if event.type == pygame.QUIT:
                run = False

            # Key Events
            if event.type == pygame.KEYDOWN:

                # Start game
                if event.key == pygame.K_SPACE and not start:
                    start = True
                    FPS = runFPS
                    # Save a deepcopy of the current grid in order if the user wants to revert
                    prevGrid = [row[:] for row in grid]

                # Reset
                elif event.key == pygame.K_r:
                    start = False
                    grid = [[False] * cols for i in range(rows)]
                    restart()
                    draw()

                # Revert
                elif event.key == pygame.K_t:

                    start = False

                    if prevGrid is None:
                        grid = [[False] * cols for i in range(rows)]
                    else:
                        grid = [row[:] for row in prevGrid]

                    restart()
                    draw()

            # Mouse Events
            if pygame.mouse.get_pressed()[0] == 1 and not start:

                mouseAction(True)

            elif pygame.mouse.get_pressed()[2] == 1 and not start:

                mouseAction(False)

        if start:
            updateGrid()

        # Update Window
        draw()

    pygame.quit()

if __name__ == "__main__":
    main()
