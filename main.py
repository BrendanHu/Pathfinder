import pygame
import sys
import math as m
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

# Initialize pygame
pygame.init()

# Create game window
screen = pygame.display.set_mode((800, 800))

# Title and icon
pygame.display.set_caption("Pathfinder") # title
# icon = pygame.image.load("sudoku.png")
# pygame.display.set_icon(icon)

# creates point class
class point:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.f = 0 # cost function (how much time/resource allocation is required)
        self.g = 0 # actual "cost" from one node to the next
        self.h = 0 # heuristic "cost" (educated guess of how far the goal node is from the new node) NOTE: h can NEVER overestimate the a
                   # or we risk getting an incorrect answer (this is fine, because the heuristic uses the straight-line distance formula)
        self.neighbours = []
        self.previous = None
        self.wall = False
        self.processed = False

    def show(self, color, margin):
        if not self.processed:
           pygame.draw.rect(screen, color, (self.i * box_width, self.j * box_length, box_width, box_length), margin)
           pygame.display.update()

    def addNeighbours(self, grid):
        if self.i > 0:
            self.neighbours.append(grid[self.i - 1][self.j])

        if self.i < columns - 1:
            self.neighbours.append(grid[self.i + 1][self.j])

        if self.j > 0:
            self.neighbours.append(grid[self.i][self.j - 1])

        if self.j < rows - 1:
            self.neighbours.append(grid[self.i][self.j + 1])

# create obstacles on mouse click
def makeWall(x, y):
    if grid[x][y] != start and grid[x][y] != end:
        if not grid[x][y].wall:
            grid[x][y].wall = True
            grid[x][y].show(orange, 0)

# heuristic used by A* to estimate most optimal route
def heuristic(a, b):
    distance = m.sqrt(m.pow(b.i - a.i, 2) + m.pow(b.j - a.j, 2))
    return distance

# grid variables and creation
rows = 50
columns = 50
grid = [0 for i in range(columns)]
for i in range(columns):
    grid[i] = [0 for i in range(rows)]

# create points on the grid
for i in range(columns):
    for j in range(rows):
        grid[i][j] = point(i, j)

# assorted variables
red = (255, 75, 75)
orange = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (192, 192, 192)
white = (255, 255, 255)
purple = (255, 8, 200)
box_width = 800 // columns
box_length = 800 // rows
path = []
done = False

# start and end points
start = grid[1][1]
end = grid[24][24]
open_set = [] # stores a list of all nodes that must still be evaluated
open_set.append(start) # base case, should the user leave the input blank
closed_set = [] # stores a list of all nodes that are already evaluated

# show squares and add neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].show(grey, 1)
        grid[i][j].addNeighbours(grid)

# make bordering walls
# for i in range(0, rows):
#     grid[0][i].show(red, 0)
#     grid[0][i].wall = True
#     grid[columns-1][i].wall = True
#     grid[columns-1][i].show(red, 0)
#     grid[i][rows-1].show(red, 0)
#     grid[i][0].show(red, 0)
#     grid[i][0].wall = True
#     grid[i][rows-1].wall = True

# ------------------------------------ MAIN LOOP FUNCTION ----------------------------------------
# Contains the A* algorithm
def main():
    # breaks the algorithm loop should there be no more points to search
    if len(open_set) != 0:
        # checks which point in open_set has the lowest f (cost function)
        lowest_index = 0
        for i in range(len(open_set)):
            if open_set[i].f < open_set[lowest_index].f:
                lowest_index = i

        current = open_set[lowest_index]
        if current == end:
            path_length = []
            for i in range(round(current.f)):
                current.processed = False
                current.show(blue, 0)
                current = current.previous
                path_length.append(0)
            end.show(purple, 0)
            # Display information for path found
            done_window = Tk()
            done_window.title("Done!")
            done_window.geometry("200x60")
            distMsg = Label(done_window, text="The shortest path is {0} blocks long.".format(len(path_length)))
            doneButton = Button(done_window, text="OK", command=done_window.destroy)

            distMsg.pack()
            doneButton.pack()

            done_window.update()
            mainloop()

            done = True
            while done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit()
        # point has been processed, add to closed_set and remove from open_set
        closed_set.append(current)
        open_set.pop(lowest_index)

        neighbours = current.neighbours
        for neighbour in neighbours:
            if neighbour not in closed_set and neighbour.wall is False:
                temp_g = current.g + 1
                if neighbour in open_set:
                    if temp_g < neighbour.g:
                        neighbour.g = temp_g
                else:
                    neighbour.g = temp_g
                    open_set.append(neighbour)

            neighbour.h = heuristic(neighbour, end)
            neighbour.f = neighbour.g + neighbour.h
            # ensure previous isn't overwritten if it already exists
            if neighbour.previous == None:
                neighbour.previous = current
    # given no solution, leave the window open and indicate this to the user
    else:
        print("No solution")
        sys.exit()
        done = True
        while done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
    # shows algorithm at work
    if checked_show_steps.get():
        for spot in open_set:
            if spot != start and spot != end:
                spot.show(green, 0)
        for spot in closed_set:
            if spot != start:
                spot.show(grey, 0)

    current.processed = True

# ------------------------------------- START/END/COORDINATE CHOICE LOOPS ------------------------------------------
user_choosing_start = True
user_choosing_end = True
user_choosing_walls = True
# Option to show algorithm visualizer
window = Tk()
window.geometry("250x80")
window.title("A* Search")
checked_show_steps = IntVar()
skip = IntVar()
showSteps = ttk.Checkbutton(window, text='Show steps ', onvalue=1, offvalue=0, variable=checked_show_steps)
skip_button = ttk.Checkbutton(window, text='Skip tutorial', onvalue=1, offvalue=0, variable=skip)

submit = Button(window, text='Let\'s go!', command=window.destroy)

showSteps.pack()
skip_button.pack()
submit.pack()

window.update()
mainloop()
# Pop-up instructions for picking a start point
if not skip.get():
    start_window = Tk()
    start_window.title("Instructions")
    start_instr = Label(start_window, text="Click on a square to pick it as the start point!")
    ok = Button(start_window, text="OK", command=start_window.destroy)

    start_instr.grid(row=0, pady=3)
    ok.grid(columnspan=6, row=3)

    start_window.update()
    mainloop()

while user_choosing_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            start_x, start_y = mouse_x // box_width, mouse_y // box_length
            if not grid[start_x][start_y].wall:
                start = grid[start_x][start_y]
            else: continue

            if start != grid[1][1]:
                open_set.pop(0)
                open_set.append(start)

            start.show(purple, 0)
            pygame.display.update()

            user_choosing_start = False

            break
# Pop-up instructions for picking an end point
if not skip.get():
    end_window = Tk()
    end_window.title("Instructions")
    end_instr = Label(end_window, text="Click on a square to pick it as the end point!")
    ok = Button(end_window, text="OK", command=end_window.destroy)

    end_instr.grid(row=0, pady=3)
    ok.grid(columnspan=6, row=3)

    end_window.update()
    mainloop()

while user_choosing_end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            end_x, end_y = mouse_x // box_width, mouse_y // box_length
            if not grid[end_x][end_y].wall:
                end = grid[end_x][end_y]
            else: continue

            end.show(purple, 0)
            pygame.display.update()

            user_choosing_end = False
            break

if not skip.get():
    wall_window = Tk()
    wall_window.title("Instructions")
    end_instr = Label(wall_window, text="Click and drag with the mouse to create walls that the algorithm must path around.\nPress SPACE to start the program!")
    ok = Button(wall_window, text="OK", command=wall_window.destroy)

    end_instr.grid(row=0, pady=3)
    ok.grid(columnspan=6, row=3)

    wall_window.update()
    mainloop()

while user_choosing_walls:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            box_x, box_y = mouse_x // box_width, mouse_y // box_length
            makeWall(box_x, box_y)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                user_choosing_walls = False
                break
        pygame.display.update()

# -------------------------------- MAIN LOOP -----------------------------------
running = True
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()
