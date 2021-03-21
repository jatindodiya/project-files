"""Djikstra's Path Finding"""

import pygame, sys, random, math
from collections import deque
from tkinter import messagebox, Tk
import os

# --------------------------------------------------------------------------------------------
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

pygame.init()

win = pygame.display.set_mode(size)
pygame.display.set_caption("Dijktdtra's Path Finding")
clock = pygame.time.Clock()

grid = []
queue, visited = deque(), []
path = []


class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        # if random.randint(0, 100) < 20:
        #     self.wall = True

    def show(self, win, col):
        if self.wall == True:
            col = (0, 0, 0)
        pygame.draw.rect(win, col, (self.x * sizeof, self.y * sizeof, sizeof - 1, sizeof - 1))

    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])

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

def removewall(pos,state):
    i = pos[0] // sizeof
    j = pos[1] // sizeof
    grid[i][j].wall = state

def place(pos):
    i = pos[0] // sizeof
    j = pos[1] // sizeof
    return i, j


for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

start = grid[20][10]
end = grid[40][20]

start.wall = False
end.wall = False

queue.append(start)
start.visited = True


def main():
    flag = False
    noflag = True
    startflag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed(3)[0]:
                    clickWall(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed(3)[2]:
                    removewall(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed(3)[0]:
                    clickWall(pygame.mouse.get_pos(), True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startflag = True

        if startflag:
            if len(queue) > 0:
                current = queue.popleft()
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

                if not flag:
                    for i in current.neighbors:
                        if not i.visited and not i.wall:
                            i.visited = True
                            i.prev = current
                            queue.append(i)
            else:
                if noflag and not flag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution")
                    noflag = False
                else:
                    continue

        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, white)
                if spot in path:
                    spot.show(win, blue)
                elif spot.visited:
                    spot.show(win, red)
                if spot in queue:
                    spot.show(win, lightblue)

                if spot == start:
                    spot.show(win, orange)
                if spot == end:
                    spot.show(win, pink)

        pygame.display.flip()


main()
