import os
import time
import argparse
from termcolor import colored
import numpy
import math

parser = argparse.ArgumentParser()
parser.add_argument('--length', '-l', required=False, action='store', type=int,
                    help='The length of each side of a shape to be drawn on Canvas with Terminal Scribe')
d = parser.parse_args()


# This is the Canvas class. It defines some height and width, and a
# matrix of characters to keep track of where the TerminalScribes are moving
class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        # This is a grid that contains data about where the 
        # TerminalScribes have visited
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    # Returns True if the given point is outside the boundaries of the Canvas
    def hitsWall(self, point):
        return point[0] < 0 or point[0] >= self._x or point[1] < 0 or point[1] >= self._y

    def middle(self, mark):
        return [round(self._x / 2), round(self._y / 2)]

    # Set the given position to the provided character on the canvas
    def setPos(self, pos, mark):
        self._canvas[pos[0]][pos[1]] = mark

    # Clear the terminal (used to create animation)
    def clear(self):
        os.system('clear')

    # Clear the terminal and then print each line in the canvas
    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))


class TerminalScribe:
    def __init__(self, canvas, angle=0):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.2
        self.pos = [0, 0]
        self.direction = [0, 1]

    def setDegrees(self, degrees):
        self.direction = [round(math.sin((degrees / 180) * math.pi)), round(-math.cos((degrees / 180) * math.pi))]

    def up(self, **kwargs):
        pos = [0, -1]
        self.forward(color=kwargs['c'])

    def down(self, **kwargs):
        pos = [0, 1]
        self.forward(color=kwargs['c'])

    def right(self, **kwargs):
        pos = [1, 0]
        self.forward(color=kwargs['c'])

    def left(self, **kwargs):
        pos = [-1, 0]
        self.forward(color=kwargs['c'])

    def draw(self, pos, color='black'):
        # Set the old position to the "trail" symbol
        self.canvas.setPos(self.pos, colored(self.trail, color))
        # Update position
        self.pos = pos
        # Set the new position to the "mark" symbol
        self.canvas.setPos(self.pos, colored(self.mark, 'black'))
        # Print everything to the screen
        self.canvas.print()
        # Sleep for a little bit to create the animation
        time.sleep(self.framerate)

    def drawShape(self, shape, sideLength=1):
        if shape == 'square':
            directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]  # right, down, left, up
        elif shape == 'triangle':
            directions = [[2, 0], [-1, -2], [-1, 2]]  # iso
        for d in directions:
            self.direction = d
            self.forward(distance=sideLength)

    def rainbow_spiral(self, cw='True'):
        self.pos = self.canvas.middle('*')  # Set position to the middle of the canvas
        rainbow = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
        length = 0
        dir_index = 0
        iteration = 1
        color_index = 0
        ind = [iteration, length, dir_index]  # , color_index]

        if cw:
            move = ['up', 'right', 'down', 'left']
        else:
            move = ['right', 'up', 'left', 'down']

        while iteration <= 20:
            if numpy.mod(iteration, 2) == 1:
                length = length + 1
            if numpy.mod(iteration, len(move)) == 1:
                dir_index = 0
            if numpy.mod(iteration, len(rainbow)) == 1:
                color_index = 0

            for l in range(length):
                self.set_line_dir(move[dir_index], c=rainbow[color_index])
            iteration = iteration + 1
            dir_index = dir_index + 1
            color_index = color_index + 1

    def set_line_dir(self, direction, **kwargs):
        if direction == 'right':
            self.trail = '-'
            self.right(**kwargs)
        elif direction == 'down':
            self.trail = '|'
            self.down(**kwargs)
        elif direction == 'left':
            self.trail = '-'
            self.left(**kwargs)
        elif direction == 'up':
            self.trail = '|'
            self.up(**kwargs)

    def forward(self, distance=1, **kwargs):
        for r in range(distance):
            pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
            if not self.canvas.hitsWall(pos):
                self.draw(pos, color='red')

# Create a new Canvas instance that is 30 units wide by 30 units tall
canvas = Canvas(30, 30)

# Create a new scribe and give it the Canvas object
scribe = TerminalScribe(canvas)

# Draw a small square
# scribe.right()
# scribe.right()
# scribe.right()
# scribe.down()
# scribe.down()
# scribe.down()
# scribe.left()
# scribe.left()
# scribe.left()
# scribe.up()
# scribe.up()
# scribe.up()

# scribe.square(size=5)
# scribe.rainbow_spiral('True')

scribes = [
    {'name' : square, 'position': [1, 1], 'degrees': 90, 'instructions': [
        {'function': 'forward', 'duration': 5},
        {'function': 'down', 'duration': 5},
        {'function': 'left', 'duration': 5},
        {'function': 'up', 'duration': 5}
        ]},
    {'name': diamond, 'position': [5, 2], 'degrees': 135, 'instructions': [
        {'function': 'forward', 'duration': 5},
        {'function': 'down', 'duration': 1},
        {'function': 'down', 'duration': 1},
        {'function': 'up', 'duration': 5}
    ]},
]