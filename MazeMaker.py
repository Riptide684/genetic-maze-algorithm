import tkinter as tk
import math
import MazeSolver


size = 500
maximum = size // 50
mode = "wall"
start = False
finish = False
colors = {
    "wall": "black",
    "path": "white",
    "start": "green",
    "finish": "red"
}
symbol = {
    "wall": "X",
    "path": "O",
    "start": "S",
    "finish": "F"
}
grid = [["O"] * maximum for _ in range(maximum)]
starting_grid = []


def initialise():
    global grid
    global starting_grid

    for i in range(0, maximum):
        canvas.create_line(i * size // maximum, size, i * size // maximum, 0)
        canvas.create_line(0, i * size // maximum, size, i * size // maximum)
        color((i*50 + 10), 40)
        color(40, (i*50 + 10))
        color((i*50 + 10), size-10)
        color(size-10, (i*50 + 10))
        grid[i][0] = "X"
        grid[0][i] = "X"
        grid[maximum-1][i] = "X"
        grid[i][maximum-1] = "X"

    starting_grid = grid.copy()


def color(x, y):
    global mode
    global start
    global finish
    global grid

    if mode == "path":
        if x < 50 or x >= size-50 or y < 50 or y >= size-50:
            return

    if mode == "start":
        if start:
            return
        else:
            start = True

    if mode == "finish":
        if finish:
            return
        else:
            finish = True

    top_left = [0, 0]
    bottom_right = [0, 0]

    top_left[0] = math.floor(x / 50) * 50
    bottom_right[0] = top_left[0] + 50
    top_left[1] = math.floor(y / 50) * 50
    bottom_right[1] = top_left[1] + 50
    canvas.create_rectangle(top_left[0], top_left[1], bottom_right[0], bottom_right[1], fill=colors[mode])
    grid[y//50][x//50] = symbol[mode]

    finish = False
    start = False

    for row in grid:
        if "F" in row:
            finish = True
        if "S" in row:
            start = True


def click(event):
    color(event.x, event.y)


def set_mode(new_mode):
    global mode
    mode = new_mode


def clear():
    global grid
    global start
    global finish
    global mode
    grid = starting_grid.copy()
    start = False
    finish = False

    for i in range(maximum):
        for j in range(maximum):
            if i == 0 or i == maximum-1 or j == 0 or j == maximum - 1:
                mode = "wall"
                color(i*50, j*50)
            else:
                mode = "path"
                color(i*50, j*50)

    mode = "wall"


def submit():
    window.withdraw()
    if start and finish:
        try:
            num1 = int(input("Enter the population size (recommended 100): "))
            num2 = int(input("Enter mutation rate as percentage (recommended 1%): "))
        except ValueError:
            print("Please enter an integer")
            window.deiconify()
            return

        window.deiconify()

        if not 3 <= num1 <= 1000:
            print("Population should be between 3 and 1000")
            return

        if not 0 <= num2 <= 100:
            print("Mutation rate should be between 0 and 100")
            return

        MazeSolver.solve(grid, num1, num2)
    else:
        print("You need a start and finish")
        window.deiconify()


window = tk.Tk()
canvas = tk.Canvas(window, bg="white", height=size, width=size)
start_button = tk.Button(window, text="Start", command=lambda: set_mode("start"))
finish_button = tk.Button(window, text="Finish", command=lambda: set_mode("finish"))
wall_button = tk.Button(window, text="Add", command=lambda: set_mode("wall"))
path_button = tk.Button(window, text="Remove", command=lambda: set_mode("path"))
submit_button = tk.Button(window, text="Submit", command=lambda: submit())
clear_button = tk.Button(window, text="Clear", command=lambda: clear())

initialise()

canvas.bind("<Button-1>", click)

canvas.pack()
start_button.pack(side=tk.LEFT)
finish_button.pack(side=tk.LEFT)
wall_button.pack(side=tk.LEFT)
path_button.pack(side=tk.LEFT)
clear_button.pack(side=tk.LEFT)
submit_button.pack(side=tk.LEFT)
window.mainloop()
