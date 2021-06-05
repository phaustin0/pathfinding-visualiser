# file for holding the tile class
import pygame
from settings import *

# class starts here
class Tile:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.colour = white
        self.neighbours = []
        self.total_rows = total_rows

    # returns position of the tile
    def get_pos(self):
        return self.row, self.col

    # checks for status of tile
    def is_closed(self):
        return self.colour == red

    def is_open(self):
        return self.colour == green

    def is_wall(self):
        return self.colour == black

    def is_start(self):
        return self.colour == orange

    def is_end(self):
        return self.colour == turquoise

    # changes the status of the tile
    def make_closed(self):
        self.colour = red

    def make_open(self):
        self.colour = green

    def make_wall(self):
        self.colour = black

    def make_start(self):
        self.colour = orange

    def make_end(self):
        self.colour = turquoise

    def make_path(self):
        self.colour = purple

    # resets the tile to its original colour -> white
    def reset(self):
        self.colour = white

    # draws the tile on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, width, width))

    # update the neighbours of the tile
    def update_neighbours(self, grid):
        self.neighbours = []  # reset the list

        # updating part
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  # up
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():  # down
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  # left
            self.neighbours.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():  # right
            self.neighbours.append(grid[self.row][self.col + 1])

    # less than operator
    def __lt__(self, other):
        return False

