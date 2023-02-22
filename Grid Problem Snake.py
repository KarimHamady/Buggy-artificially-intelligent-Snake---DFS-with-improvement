import random
import pygame as py
import sys

color_of_initial_and_target = "blue"
color_of_grid_background = "green"
color_of_screen_background = "black"
color_of_block_border = (10, 10, 10)
color_of_fs = "pink"
color_of_path = "yellow"
color_of_obstacles = "red"
color_of_snake = "green"
block_size = 60
screen_size = (1350, 650)
grid_size = screen_size
grid_shift = ((screen_size[0] - grid_size[0]) // 2, screen_size[1] - grid_size[1] - 20)
display = py.display.set_mode((screen_size[0], screen_size[1]))
display.fill(color_of_screen_background)


class Snake:
    body = []

    def __init__(self):
        self.body.append((0, 0))

    def eat_apple(self, current_position):
        self.body.append(current_position)

    def draw_snake(self, current_position):
        removed_block_from_snake = self.body.pop(0)
        draw_rect_at_current_position(removed_block_from_snake, color_of_screen_background)
        self.body.append(current_position)
        for block in self.body:
            rect = py.Rect(block[0]*block_size + grid_shift[0],
                           block[1]*block_size + grid_shift[1],
                           block_size,
                           block_size)
            py.draw.rect(display, color_of_snake, rect)
            py.display.update()
        py.time.wait(20)


class Grid:

    def __init__(self):
        self.number_of_obstacles = 20
        self.grid_dimensions = (grid_size[0] // block_size, grid_size[1] // block_size)
        self.grid = self.generate_grid()

    def generate_grid(self):
        no_obstacles_grid = [[1000 for _ in range(self.grid_dimensions[1])] for _ in range(self.grid_dimensions[0])]
        for _ in range(self.number_of_obstacles):
            rand_x = random.randint(0, self.grid_dimensions[0] - 1)
            rand_y = random.randint(0, self.grid_dimensions[1] - 1)
            no_obstacles_grid[rand_x][rand_y] = -1
        py.display.update()
        return no_obstacles_grid

    def draw_grid(self):
        for x in range(0, self.grid_dimensions[0]):
            for y in range(0, self.grid_dimensions[1]):
                rect = py.Rect(x*block_size + grid_shift[0], y*block_size + grid_shift[1], block_size, block_size)
                if self.grid[x][y] == -1:
                    py.draw.rect(display, color_of_obstacles, rect)
                else:
                    py.draw.rect(display, color_of_block_border, rect, 1)
        py.display.update()


def initialize_beginning():
    position_initialized = False
    while not position_initialized:
        for event in py.event.get():
            if event.type == py.MOUSEBUTTONDOWN:
                mouse_location = py.mouse.get_pos()
                print("Mouse" + str(mouse_location))
                user_initial_position = [0, 0]
                user_initial_position[0] = \
                    (mouse_location[0] - mouse_location[0] % block_size - grid_shift[0]) // block_size
                user_initial_position[1] = \
                    (mouse_location[1] - mouse_location[1] % block_size - grid_shift[1]) // block_size
                print("Initial_position" + str(user_initial_position))
                return tuple(user_initial_position)


def optimal_movements(initial_pos, target_pos):
    directions = {"down": (1, 0), "left": (0, -1), "up": (-1, 0), "right": (0, 1)}
    difference_tuple = tuple(map(lambda i, t: i - t, initial_pos, target_pos))
    movement = ["right", "down", "left", "up"]
    if difference_tuple[0] > 0:
        if difference_tuple[1] > 0:
            # movement = ["down", "right", "up", "left"]
            movement = ["right", "down", "left", "up"]
        elif difference_tuple[1] < 0:
            movement = ["down", "left", "up", "right"]
        else:
            movement = ["down", "right", "up", "left"]
    elif difference_tuple[0] < 0:
        if difference_tuple[1] > 0:
            movement = ["right", "up", "left", "down"]
        elif difference_tuple[1] < 0:
            movement = ["up", "left", "down", "right"]
        else:
            movement = ["left", "up", "right", "down"]
    else:
        if difference_tuple[1] > 0:
            movement = ["down", "right", "up", "left"]
        elif difference_tuple[1] < 0:
            movement = ["up", "left", "down", "right"]
    return list(map(lambda direction: directions[direction], movement))


def check_events():
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()


def draw_rect_at_current_position(current_position, color):
    rect = py.Rect(current_position[0] * block_size + grid_shift[0],
                   current_position[1] * block_size + grid_shift[1],
                   block_size,
                   block_size)
    py.draw.rect(display, color, rect)
    py.draw.rect(display, color_of_block_border, rect, 1)
    py.display.update()
    check_events()


def draw_path(path):
    for position in path:
        draw_rect_at_current_position(position, color_of_path)


def fs_grid(breadth, grid, initial_position, target_position, array_dimensions):
    visited = []
    queue = []
    steps = 0
    current_position = initial_position
    queue.append(current_position)
    visited.append(current_position)
    while queue:
        if breadth:
            cur = queue.pop(0)
        else:
            cur = queue.pop()
        snake.draw_snake(cur)
        draw_rect_at_current_position(target_position, color_of_initial_and_target)
        possible_movements = optimal_movements(cur, target_position)
        for movement in possible_movements:
            new_position = (cur[0] + movement[0], cur[1] + movement[1])
            if 0 <= new_position[0] <= array_dimensions[0] - 1 \
                    and 0 <= new_position[1] <= array_dimensions[1] - 1 \
                    and (new_position not in visited) \
                    and grid[new_position[0]][new_position[1]] != -1:
                grid[new_position[0]][new_position[1]] = steps
                queue.append(new_position)
                visited.append(new_position)
                steps += 1
                if new_position == target_position:
                    snake.eat_apple(new_position)
                    return True
                # draw_rect_at_current_position(new_position, color_of_fs)
    return False


py.init()
display.fill(color_of_screen_background)
initial_position = (0, 0)
target_position = (10, 0)
snake = Snake()
grid_object = Grid()
display.fill(color_of_screen_background)
grid_object.draw_grid()
while True:
    start = False
    draw_rect_at_current_position(target_position, color_of_initial_and_target)
    found = fs_grid(False, grid_object.grid, initial_position, target_position, grid_object.grid_dimensions)
    draw_rect_at_current_position(target_position, color_of_screen_background)
    initial_position = snake.body[-1]
    target_x = random.randint(0, grid_object.grid_dimensions[0] - 1)
    target_y = random.randint(0, grid_object.grid_dimensions[1] - 1)
    target_position = (target_x, target_y)
    check_events()
