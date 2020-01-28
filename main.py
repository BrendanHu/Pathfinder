import os
import sys
import math as m
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pygame
import time

# Changes user's working directory to the location of the file (only really matters in Atom, in my experience)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Ensures screen shows in the same place every time
screen_x = 100
screen_y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "{0},{1}".format(screen_x, screen_y)
# Initialize pygame
pygame.init()
# Create game window
screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
# Title and icon
pygame.display.set_caption("Pathfinder")
# icon = pygame.image.load("sudoku.png")
# pygame.display.set_icon(icon)


class point:
    """Creates an object representing a point (square) on the grid."""
    def __init__(self, i, j):
        """Point properties."""
        self.i = i
        self.j = j
        # cost function (how much time/resource allocation is required)
        self.f = 0
        # actual "cost" from one node to the next
        self.g = 0
        # heuristic "cost" (educated guess of how far the goal node is from the new node)
        self.h = 0
        self.neighbours = []
        self.previous = None
        self.wall = False
        self.processed = False

    def show(self, color, grid_thickness):
        if not self.processed:
            pygame.draw.rect(screen, color, (self.i * box_width, self.j * box_length, box_width, box_length), grid_thickness)
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

    def __repr__(self):
        """Representation of a point for debugging."""
        return "Point with x = {}, y = {}".format(self.i, self.j)


def makeWall(x, y):
    """Creates obstacles on mouse click, given x and y coordinates."""
    if grid[x][y] != start and grid[x][y] != end:
        if not grid[x][y].wall:
            grid[x][y].wall = True
            grid[x][y].show(wall_color, 0)


def heuristic(a, b):
    """Heuristic used by the A* search algorithm."""
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
gold = (255, 234, 171)  # closed set colour
wall_color = (0, 0, 0)
green = (100, 255, 150)  # open set colour
path_colour = (171, 192, 255)
grey = (112, 128, 144)  # grid colour
off_white = (240, 255, 255)  # screen colour
box_width = 800 // columns
box_length = 800 // rows
path = []
done = False

# makes the background off-white
screen.fill(off_white)

# initializes lists for open set and closed set
open_set = []  # stores a list of all nodes that must still be evaluated
closed_set = []  # stores a list of all nodes that are already evaluated

# show squares and add neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].show(grey, 1)
        grid[i][j].addNeighbours(grid)

# ------------------------------------ MAIN LOOP FUNCTION ----------------------------------------


def main():
    global open_set
    global closed_set
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
            end_time = time.perf_counter()
            path_length = 0
            # Calculates and renders path on screen
            for i in range(round(current.f)):
                current.processed = False
                if not current == end:
                    current.show(path_colour, 0)
                current = current.previous
                path_length += 1

            # Display information for path found
            # TODO: Find a way to let the user exit without clicking the ok button
            done_window = Tk()
            done_window.title("Done!")
            done_window.geometry("500x125+250+450")
            distMsg = Label(done_window, text="The shortest path is {0} blocks long.".format(path_length) +
                                            "\nTime elapsed: {0:0.2f} seconds".format(end_time - start_time) +
                                            "\n If you want, press R to restart!")
            distMsg.config(font=("Arial", 18, "bold"))
            doneButton = Button(done_window, text="OK", command=done_window.destroy)

            distMsg.pack()
            doneButton.pack()

            done_window.update()
            mainloop()

            done = True
            while done is True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        # makes the background off-white
                        screen.fill(off_white)
                        # create points on the grid
                        for i in range(columns):
                            for j in range(rows):
                                grid[i][j] = point(i, j)
                        # show squares and add neighbours
                        for i in range(columns):
                            for j in range(rows):
                                grid[i][j].show(grey, 1)
                                grid[i][j].addNeighbours(grid)
                        startApp()
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
            # ensure previous isn't overwritten if it already exists,
            # then gives the next square the previous of the current one
            if neighbour.previous is None:
                neighbour.previous = current
    # given no solution, leave the window open and indicate this to the user
    else:
        end_time = time.perf_counter()
        done_window = Tk()
        done_window.title("Done!")
        done_window.geometry("375x125+400+450")
        distMsg = Label(done_window, text="There is no path!  :(\nTime elapsed: {0:0.2f} seconds\nIf you want, press R to restart!".format(end_time - start_time))
        distMsg.config(font=("Arial", 18, "bold"))
        doneButton = Button(done_window, text="OK", command=done_window.destroy)

        distMsg.pack()
        doneButton.pack()

        done_window.update()
        mainloop()

        done = True
        while done is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    # makes the background off-white
                    screen.fill(off_white)
                    # create points on the grid
                    for i in range(columns):
                        for j in range(rows):
                            grid[i][j] = point(i, j)
                    # show squares and add neighbours
                    for i in range(columns):
                        for j in range(rows):
                            grid[i][j].show(grey, 1)
                            grid[i][j].addNeighbours(grid)
                    startApp()
    # shows algorithm at work
    if checked_show_steps.get():
        for spot in open_set:
            if spot not in (start, end):
                spot.show(green, 0)
        for spot in closed_set:
            if spot != start:
                spot.show(gold, 0)

    current.processed = True


def startApp():
    """
    Contains the game start user interface and a call to main().
    """
    global start
    global end
    global checked_show_steps
    global start_time
    global end_time
    global open_set
    global closed_set

    open_set = []
    closed_set = []
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

    user_choosing_start = True
    start = grid[0][0]
    start_image = pygame.image.load("home.png")
    while user_choosing_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                # Gets location of the click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                start_x, start_y = mouse_x // box_width, mouse_y // box_length

                # Marks start point to user
                screen.blit(start_image, (start_x * box_width, start_y * box_length))

                # Sets start point
                start = grid[start_x][start_y]
                open_set.append(start)
                """ TODO: Try to make start movable after placement. """
                # if len(open_set) > 1:
                #     if open_set[0] != open_set[1]:
                #         screen.fill(off_white, pygame.Rect(open_set[0].i * box_width, open_set[0].j * box_length, box_width-5, box_length-5))
                #         open_set[0].show(off_white, 2)
                #         # screen.blit(background_colour, pygame.Rect(open_set[0].i * box_width, open_set[0].j * box_length, 100, 100),
                #         # pygame.Rect(open_set[0].i * box_width, open_set[0].j * box_length, box_width, box_length))
                #
                #         pygame.display.update()
                #         print("Showing white at old start")
                #     open_set.pop(0)

                pygame.display.update()
                user_choosing_start = False
                break

            # if event.type == pygame.MOUSEBUTTONUP:
                # intending to move the break and var change down here once above is done


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

    user_choosing_end = True
    end_image = pygame.image.load("finish.png")
    while user_choosing_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                # Gets position of clickscreen.blit(start_image, (start_x * box_width, start_y * box_length))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                end_x, end_y = mouse_x // box_width, mouse_y // box_length

                # Sets end point
                if not grid[end_x][end_y].wall and grid[start_x][start_y] != grid[end_x][end_y]:
                    end = grid[end_x][end_y]
                    screen.blit(end_image, (end_x * box_width, end_y * box_length))
                else:
                    continue

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

    user_choosing_walls = True
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

                    start_time = time.perf_counter()
                    running = True
                    while running is True:
                        event = pygame.event.poll()
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        pygame.display.update()
                        main()

                    break
            pygame.display.update()

# -------------------------------- MAIN LOOP -----------------------------------
startApp()
