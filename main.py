import os
import sys
import math as m
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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
    # Manhattan distance can be used as an alternative to the straight line formula
    # distance = abs(a.i - b.i) + abs(a.j - b.j) TODO: if this is used, I'd have to figure out diagonals
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
open_set = []  # stores a list of all nodes that must still be evaluated
open_set.append(start)  # base case, should the user leave the input blank
closed_set = []  # stores a list of all nodes that are already evaluated

# show squares and add neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].show(grey, 1)
        grid[i][j].addNeighbours(grid)

# ------------------------------------ MAIN LOOP FUNCTION ----------------------------------------


def main():
    """Contains the A* algorithm."""
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
            # TODO: Find a way to let the user exit without clicking the ok button
            done_window = Tk()
            done_window.title("Done!")
            done_window.geometry("500x80+250+450")
            distMsg = Label(done_window, text="The shortest path is {0} blocks long.".format(len(path_length)))
            distMsg.config(font=("Arial", 18, "bold"))
            doneButton = Button(done_window, text="OK", command=done_window.destroy)

            distMsg.pack()
            doneButton.pack()

            done_window.update()
            mainloop()

            done = True
            while done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
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
            if neighbour.previous is None:
                neighbour.previous = current
    # given no solution, leave the window open and indicate this to the user
    else:
        done_window = Tk()
        done_window.title("Done!")
        done_window.geometry("250x80+400+450")
        distMsg = Label(done_window, text="There is no path!  :(")
        distMsg.config(font=("Arial", 18, "bold"))
        doneButton = Button(done_window, text="OK", command=done_window.destroy)

        distMsg.pack()
        doneButton.pack()

        done_window.update()
        mainloop()
        done = True
        while done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
    # shows algorithm at work
    if checked_show_steps.get():
        for spot in open_set:
            if spot not in (start, end):
                spot.show(green, 0)
        for spot in closed_set:
            if spot != start:
                spot.show(grey, 0)

    current.processed = True


# ------------------------------------- START/END/COORDINATE CHOICE LOOPS ------------------------------------------
user_choosing_start = True
user_choosing_end = True
user_choosing_walls = True
# Option to show algorithm visualizer and skip the tutorial
window = Tk()
window.geometry("250x80+400+200")
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
    start_window.geometry("350x80+350+70")
    start_instr = Label(start_window, text="Click on a square to pick\nit as the start point!")
    start_instr.config(font=("Arial", 16, "bold"))
    ok = Button(start_window, text="OK", command=start_window.destroy)

    start_instr.pack()
    ok.pack()

    start_window.update()
    mainloop()

while user_choosing_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            start_x, start_y = mouse_x // box_width, mouse_y // box_length
            if not grid[start_x][start_y].wall:
                start = grid[start_x][start_y]
            else:
                continue

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
    end_window.geometry("350x80+350+70")
    end_instr = Label(end_window, text="Click on a square to\npick it as the end point!")
    end_instr.config(font=("Arial", 16, "bold"))
    ok = Button(end_window, text="OK", command=end_window.destroy)

    end_instr.pack()
    ok.pack()

    end_window.update()
    mainloop()

while user_choosing_end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            end_x, end_y = mouse_x // box_width, mouse_y // box_length
            if not grid[end_x][end_y].wall and grid[start_x][start_y] != grid[end_x][end_y]:
                end = grid[end_x][end_y]
            else:
                continue

            end.show(purple, 0)
            pygame.display.update()

            user_choosing_end = False
            break

if not skip.get():
    wall_window = Tk()
    wall_window.title("Instructions")
    wall_window.geometry("800x70+100+90")
    wall_instr = Label(wall_window, text="Click and drag with the mouse to create walls that the "
                       "algorithm must path around.\nPress SPACE to start the program!")
    wall_instr.config(font=("Arial", 14, "bold"))
    ok = Button(wall_window, text="OK", command=wall_window.destroy)

    wall_instr.pack()
    ok.pack()

    wall_window.update()
    mainloop()

while user_choosing_walls:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
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
