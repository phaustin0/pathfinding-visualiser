# main file to handle everything

###############
### Imports ###
###############
import pygame
import math
from queue import PriorityQueue
from tile import Tile
from settings import *


#########################
### Initialise PyGame ###
#########################
pygame.init()


##################################
### Create and name the window ###
##################################
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(title)


#################
### Functions ###
#################

# heuristic function
def h(p1, p2):
    # get the x, y coordinates of each point
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)  # returns manhattan distance between the points

# create the grid
def create_grid(rows, width):
    grid = []
    tile_width = width // rows
    # creation of the grid with all of the tile objects
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            tile = Tile(i, j, tile_width, rows)
            grid[i].append(tile)
    
    # return the grid at the end
    return grid

# draw the grid lines
def draw_grid(screen, rows, width):
    tile_width = width // rows
    for i in range(rows):
        # draw horizontal lines
        pygame.draw.line(screen, grey, (0, i * tile_width), (width, i * tile_width))
        for j in range(rows):
            # draw vertical lines
            pygame.draw.line(screen, grey, (j * tile_width, 0), (j * tile_width, width))

# draw everything
def draw(screen, grid, rows, width):
    # draw background
    screen.fill(white)

    # colour in all of the tiles
    for row in grid:
        for tile in row:
            tile.draw(screen)

    # draw the grid lines
    draw_grid(screen, rows, width)

    # update the screen
    pygame.display.update()

# get position of the mouse when clicked in terms of the grid array
def get_clicked_pos(pos, rows, width):
    tile_width = width // rows
    y, x = pos

    row = y // tile_width
    col = x // tile_width
    return row, col

# main function / loop
def main(screen, width):
    rows = 50
    # create the grid
    grid = create_grid(rows, width)

    # start and end positions
    start = None
    end = None

    # is the application running?
    is_running = True
    
    # main loop
    while is_running:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            # mouse clicking
            if pygame.mouse.get_pressed()[0]:    # left mouse button
                # get mouse position
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)

                # selected tile
                tile = grid[row][col]

                # placing tiles
                if not start and tile != end:
                    start = tile
                    start.make_start()

                elif not end and tile != start:
                    end = tile
                    end.make_end()

                elif tile != start and tile != end:
                    tile.make_wall()

            elif pygame.mouse.get_pressed()[2]:  # right mouse button
                # get mouse position
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)

                # selected tile
                tile = grid[row][col]
                tile.reset()  # reset the tile

                # checks
                if tile == start:
                    start = None
                elif tile == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # update neighbours of each tile in the grid
                    for row in grid:
                        for tile in row:
                            tile.update_neighbours(grid)

                    # algorithm
                    alg(lambda: draw(screen, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    # clear the screen and reset everything
                    start = end = None
                    grid = create_grid(rows, width)  # recreate the grid

        # draw and update the screen
        draw(screen, grid, rows, width)

    # quit out of the window
    pygame.quit()

# algorithm
def alg(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_scores = {tile: float('inf') for row in grid for tile in row}
    g_scores[start] = 0
    f_scores = {tile: float('inf') for row in grid for tile in row}
    f_scores[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]  # get the current node
        open_set_hash.remove(current)

        if current == end:
            current.make_end()
            find_path(came_from, end, start, draw)
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_scores[current] + 1
            # update g score of neighbour
            if temp_g_score < g_scores[neighbour]:
                came_from[neighbour] = current
                g_scores[neighbour] = temp_g_score
                f_scores[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_scores[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open() if neighbour != end else neighbour.make_end()
        draw()

        if current != start:
            current.make_closed()

    return False

# find the most optimal path
def find_path(came_from, current, start, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path() if current != start else current.make_start()
        draw()

# run the file
if __name__ == "__main__":
    main(screen, width)

