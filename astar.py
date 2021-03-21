import pygame, sys, random, math
from tkinter import messagebox, Tk
import os

# -----------------------------------color define-----------------------------------------
red = (178, 34, 34)
orange = (255, 110, 0)
lightblue = (30, 144, 255)
blue = (25, 25, 112)
pink = (255, 105, 180)
black = (0, 0, 0)
aqua = (32, 178, 170)
white = (220, 220, 220)

# --------------------------------------------------------------------------------------------
# number between 2 - 200
sizeofarr = 50
showgrid = 1
if sizeofarr >= 150:
    showgrid = 0  # only 1 or 0
# --------------------------------------------------------------------------------------------
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30, 30)
root = Tk()
root.title("Start Window")
# root.iconbitmap('pyc.ico')
screen_width = root.winfo_screenwidth() - 50  # screen window width
screen_height = root.winfo_screenheight() - 100  # screen window height

screen_height = screen_height - screen_height % sizeofarr
sizeof = screen_height // sizeofarr
screen_width = screen_width - screen_width % sizeof

# -----------------------------------------------------------------------------------------
width = screen_width
height = screen_height

size = (width, height + 30)

pygame.init()
win = pygame.display.set_mode(size)
clock = pygame.time.Clock()

rows = sizeofarr
cols = screen_width // sizeof
print(rows, cols)

# ------------------------------------------------------------------------------------

grid = []
openSet, closeSet = [], []
path = []

w = width // cols
h = height // rows
print(w, h)


class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        # if random.randint(0, 100) < 20:
        #     self.wall = True

    def show(self, win, col):
        if self.wall == True:
            col = (0, 0, 0)
        pygame.draw.rect(win, col, (self.x * w, self.y * h, w - 1, h - 1))

    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        # Add Diagonals
        if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y + 1])
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x + 1][self.y - 1])
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x - 1][self.y + 1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x - 1][self.y - 1])


def clickWall(pos, state):
    i = pos[0] // sizeof
    j = pos[1] // sizeof
    grid[i][j].wall = state


def place(pos):
    i = pos[0] // sizeof
    j = pos[1] // sizeof
    return i, j


def heuristics(a, b):
    return math.sqrt((a.x - b.x) ** 2 + abs(a.y - b.y) ** 2)


def displayMessage(message):  # message box
    fonts = pygame.font.SysFont('comicsans', 40)
    pygame.draw.rect(win, pink, (0, screen_height, screen_width, 30))
    win.blit(fonts.render(message, True, blue), (20, screen_height + 3))
    pygame.display.update()


for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

start = grid[2][2]
end = grid[20][10]

openSet.append(start)


def close():
    pygame.quit()
    sys.exit()


def main():
    flag = False
    noflag = True
    startflag = False
    displayMessage("astar algorithm")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed(3)[0]:
                    clickWall(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed(3)[2]:
                    clickWall(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    clickWall(pygame.mouse.get_pos(), True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startflag = True

        if startflag:
            if len(openSet) > 0:
                winner = 0
                for i in range(len(openSet)):
                    if openSet[i].f < openSet[winner].f:
                        winner = i

                current = openSet[winner]

                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev
                    if not flag:
                        flag = True
                        print("Done")
                    elif flag:
                        continue

                if flag == False:
                    openSet.remove(current)
                    closeSet.append(current)

                    for neighbor in current.neighbors:
                        if neighbor in closeSet or neighbor.wall:
                            continue
                        tempG = current.g + 1

                        newPath = False
                        if neighbor in openSet:
                            if tempG < neighbor.g:
                                neighbor.g = tempG
                                newPath = True
                        else:
                            neighbor.g = tempG
                            newPath = True
                            openSet.append(neighbor)

                        if newPath:
                            neighbor.h = heuristics(neighbor, end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.prev = current

            else:
                if noflag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution")
                    noflag = False

        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, white)
                if flag and spot in path:
                    spot.show(win, blue)
                elif spot in closeSet:
                    spot.show(win, red)
                elif spot in openSet:
                    spot.show(win, lightblue)
                try:
                    if spot == start:
                        spot.show(win, orange)
                    if spot == end:
                        spot.show(win, pink)
                except Exception:
                    pass

        pygame.display.flip()


main()
