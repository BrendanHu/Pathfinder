<<<<<<< HEAD
import os
=======
import pygame
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
import sys
import math as m
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
<<<<<<< HEAD
import pygame
# Ensure screen shows in the same place every time
screen_x = 100
screen_y = 200
os.environ['SDL_VIDEO_WINDOW_POS'] = "{0},{1}".format(screen_x, screen_y)
# Initialize pygame
pygame.init()
# Create game window
screen = pygame.display.set_mode((800, 800))
# Title and icon
pygame.display.set_caption("Pathfinder")
# icon = pygame.image.load("sudoku.png")
# pygame.display.set_icon(icon)


class point:
    """Creates an object representing a point (square) on the grid."""
    def __init__(self, i, j):
        self.i = i
        self.j = j
        # cost function (how much time/resource allocation is required)
        self.f = 0
        # actual "cost" from one node to the next
        self.g = 0
        # heuristic "cost" (educated guess of how far the goal node is from the new node) NOTE: h can NEVER overestimate the a
        # or we risk getting an incorrect answer (this is fine, because the heuristic uses the straight-line distance formula)
        self.h = 0
=======
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
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
        self.neighbours = []
        self.previous = None
        self.wall = False
        self.processed = False

    def show(self, color, margin):
        if not self.processed:
<<<<<<< HEAD
            pygame.draw.rect(screen, color, (self.i * box_width, self.j * box_length, box_width, box_length), margin)
            pygame.display.update()
=======
           pygame.draw.rect(screen, color, (self.i * box_width, self.j * box_length, box_width, box_length), margin)
           pygame.display.update()
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373

    def addNeighbours(self, grid):
        if self.i > 0:
            self.neighbours.append(grid[self.i - 1][self.j])

        if self.i < columns - 1:
            self.neighbours.append(grid[self.i + 1][self.j])

        if self.j > 0:
            self.neighbours.append(grid[self.i][self.j - 1])

        if self.j < rows - 1:
            self.neighbours.append(grid[self.i][self.j + 1])

<<<<<<< HEAD

=======
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
# create obstacles on mouse click
def makeWall(x, y):
    if grid[x][y] != start and grid[x][y] != end:
        if not grid[x][y].wall:
            grid[x][y].wall = True
            grid[x][y].show(orange, 0)

<<<<<<< HEAD

=======
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
# heuristic used by A* to estimate most optimal route
def heuristic(a, b):
    distance = m.sqrt(m.pow(b.i - a.i, 2) + m.pow(b.j - a.j, 2))
    return distance

<<<<<<< HEAD

=======
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
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
<<<<<<< HEAD
open_set = []  # stores a list of all nodes that must still be evaluated
open_set.append(start)  # base case, should the user leave the input blank
closed_set = []  # stores a list of all nodes that are already evaluated
=======
open_set = [] # stores a list of all nodes that must still be evaluated
open_set.append(start) # base case, should the user leave the input blank
closed_set = [] # stores a list of all nodes that are already evaluated
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373

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
<<<<<<< HEAD


def main():
    """Contains the A* algorithm."""
=======
# Contains the A* algorithm
def main():
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
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
<<<<<<< HEAD
            done_window.geometry("500x80+250+450")
            distMsg = Label(done_window, text="The shortest path is {0} blocks long.".format(len(path_length)))
            distMsg.config(font=("Arial", 18, "bold"))
=======
            done_window.geometry("200x60")
            distMsg = Label(done_window, text="The shortest path is {0} blocks long.".format(len(path_length)))
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
            doneButton = Button(done_window, text="OK", command=done_window.destroy)

            distMsg.pack()
            doneButton.pack()

            done_window.update()
            mainloop()

            done = True
            while done:
                for event in pygame.event.get():
<<<<<<< HEAD
                    if event.type == pygame.QUIT:
                        sys.exit()
=======
                    if event.type == pygame.QUIT: sys.exit()
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
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
<<<<<<< HEAD
            if neighbour.previous is None:
=======
            if neighbour.previous == None:
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
                neighbour.previous = current
    # given no solution, leave the window open and indicate this to the user
    else:
        print("No solution")
        sys.exit()
        done = True
        while done:
            for event in pygame.event.get():
<<<<<<< HEAD
                if event.type == pygame.QUIT:
                    sys.exit()
    # shows algorithm at work
    if checked_show_steps.get():
        for spot in open_set:
            if spot not in (start, end):
=======
                if event.type == pygame.QUIT: sys.exit()
    # shows algorithm at work
    if checked_show_steps.get():
        for spot in open_set:
            if spot != start and spot != end:
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
                spot.show(green, 0)
        for spot in closed_set:
            if spot != start:
                spot.show(grey, 0)

    current.processed = True

<<<<<<< HEAD

=======
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
# ------------------------------------- START/END/COORDINATE CHOICE LOOPS ------------------------------------------
user_choosing_start = True
user_choosing_end = True
user_choosing_walls = True
<<<<<<< HEAD
# Option to show algorithm visualizer and skip the tutorial
window = Tk()
window.geometry("250x80+400+200")
=======
# Option to show algorithm visualizer
window = Tk()
window.geometry("250x80")
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
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
<<<<<<< HEAD
    start_window.geometry("350x80+350+70")
    start_instr = Label(start_window, text="Click on a square to pick\nit as the start point!")
    start_instr.config(font=("Arial", 16, "bold"))
    ok = Button(start_window, text="OK", command=start_window.destroy)

    start_instr.pack()
    ok.pack()
=======
    start_instr = Label(start_window, text="Click on a square to pick it as the start point!")
    ok = Button(start_window, text="OK", command=start_window.destroy)

    start_instr.grid(row=0, pady=3)
    ok.grid(columnspan=6, row=3)
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373

    start_window.update()
    mainloop()

while user_choosing_start:
    for event in pygame.event.get():
<<<<<<< HEAD
        if event.type == pygame.QUIT:
            sys.exit()
=======
        if event.type == pygame.QUIT: sys.exit()
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            start_x, start_y = mouse_x // box_width, mouse_y // box_length
            if not grid[start_x][start_y].wall:
                start = grid[start_x][start_y]
<<<<<<< HEAD
            else:
                continue
=======
            else: continue
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373

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
<<<<<<< HEAD
    end_window.geometry("350x80+350+70")
    end_instr = Label(end_window, text="Click on a square to\npick it as the end point!")
    end_instr.config(font=("Arial", 16, "bold"))
    ok = Button(end_window, text="OK", command=end_window.destroy)

    end_instr.pack()
    ok.pack()
=======
    end_instr = Label(end_window, text="Click on a square to pick it as the end point!")
    ok = Button(end_window, text="OK", command=end_window.destroy)

    end_instr.grid(row=0, pady=3)
    ok.grid(columnspan=6, row=3)
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373

    end_window.update()
    mainloop()

while user_choosing_end:
    for event in pygame.event.get():
<<<<<<< HEAD
        if event.type == pygame.QUIT:
            sys.exit()
=======
        if event.type == pygame.QUIT: sys.exit()
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            end_x, end_y = mouse_x // box_width, mouse_y // box_length
            if not grid[end_x][end_y].wall:
                end = grid[end_x][end_y]
<<<<<<< HEAD
            else:
                continue
=======
            else: continue
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373

            end.show(purple, 0)
            pygame.display.update()

            user_choosing_end = False
            break

if not skip.get():
    wall_window = Tk()
    wall_window.title("Instructions")
<<<<<<< HEAD
    wall_window.geometry("800x70+100+90")
    wall_instr = Label(wall_window, text="Click and drag with the mouse to create walls that the "
                       "algorithm must path around.\nPress SPACE to start the program!")
    wall_instr.config(font=("Arial", 14, "bold"))
    ok = Button(wall_window, text="OK", command=wall_window.destroy)

    wall_instr.pack()
    ok.pack()
=======
    end_instr = Label(wall_window, text="Click and drag with the mouse to create walls that the algorithm must path around.\nPress SPACE to start the program!")
    ok = Button(wall_window, text="OK", command=wall_window.destroy)

    end_instr.grid(row=0, pady=3)
    ok.grid(columnspan=6, row=3)
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373

    wall_window.update()
    mainloop()

while user_choosing_walls:
    for event in pygame.event.get():
<<<<<<< HEAD
        if event.type == pygame.QUIT:
            sys.exit()
=======
        if event.type == pygame.QUIT: sys.exit()
>>>>>>> b79ae167a80e407e465801000cc6e67c9821f373
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
