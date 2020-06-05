import collections
import random
import sys
import tkinter as tk

import q

SCREEN_WIDTH = 30
SCREEN_HEIGHT = 15

SCALE = 20

DIRECTIONS = {
    'Up': {
        'coords': {
            'x': 0,
            'y': -1
        },
        'forbidden': 'Down'
    },
    'Down': {
        'coords': {
            'x': 0,
            'y': 1
        },
        'forbidden': 'Up'
    },
    'Left': {
        'coords': {
            'x': -1,
            'y': 0
        },
        'forbidden': 'Right'
    },
    'Right': {
        'coords': {
            'x': 1,
            'y': 0
        },
        'forbidden': 'Left'
    }
}


class SnakeGame:

    def __init__(self, canvas):
        self.canvas = canvas
        self.snake_body = self.init_body()
        self.food_counter = 0
        self.food = self.make_food()
        self.current_direction = 'Right'
        self.next_direction = 'Right'
        self.crawl()
        
    def crawl(self):
        """
        Crawls one step at a time and eats food if on the way.
        Takes care of colliding with itself, too.
        """
        self.current_direction = self.next_direction
        self.food_counter += 100

        if self.food_counter == 5000:
            self.food_counter = 0
            self.food = self.make_food()

        next_step = self.get_next_step()
        if next_step == self.food:
            self.eat_food()
        elif next_step in self.snake_body:
            sys.exit()
        else:
            self.snake_body.append(next_step)

        self.draw_snake()
        self.canvas.after(100, self.crawl)
    
    def eat_food(self):
        """
        Eats food on the way and grows snake body by a piece.
        """
        self.food_counter = 0
        self.snake_body = collections.deque(self.snake_body, maxlen=self.snake_body.maxlen+1)
        self.snake_body.insert(0, (
            self.snake_body[0][0] + DIRECTIONS[self.current_direction]['coords']['x'],
            self.snake_body[0][1] + DIRECTIONS[self.current_direction]['coords']['y']
        ))
        self.food = self.make_food()

    def make_food(self):
        """
        Makes food until it is positioned properly.
        """
        self.canvas.delete('food')
        while True:
            x = random.randrange(SCREEN_WIDTH)
            y = random.randrange(SCREEN_HEIGHT)
            if not (x, y) in self.snake_body:
                break
        self.draw_food(x, y)
        return (x, y)

    def draw_snake(self):
        """
        Draws snake body on the canvas.
        """
        self.canvas.delete('!food')
        for piece in self.snake_body:
            self.canvas.create_rectangle(
                piece[0] * SCALE, piece[1] * SCALE,
                (piece[0] + 1) * SCALE, (piece[1] + 1) * SCALE,
                fill='black'
            )
    
    def draw_food(self, x, y):
        """
        Draws food on the canvas.
        """
        self.canvas.create_rectangle(
            x * SCALE, y * SCALE,
            (x + 1) * SCALE, (y + 1) * SCALE,
            fill='red', tags=['food']
        )

    def init_body(self):
        """
        Initializes snake body.
        """
        return collections.deque(
            [(SCREEN_WIDTH // 2 + i, SCREEN_HEIGHT // 2) for i in range(-3, 4)],
            maxlen=7
        )

    def get_next_step(self):
        """
        Gets next step based on current direction in (X, Y) form.
        """
        return (
            (self.snake_body[-1][0] + DIRECTIONS[self.current_direction]['coords']['x']) % SCREEN_WIDTH,
            (self.snake_body[-1][1] + DIRECTIONS[self.current_direction]['coords']['y']) % SCREEN_HEIGHT
        )

    def set_direction(self, event):
        """
        Sets direction whilst making sure it isn't the forbidden one.
        """
        direction = event.keysym
        if direction != DIRECTIONS[self.current_direction]['forbidden']:
            self.next_direction = direction


def main():
    root = tk.Tk()
    canvas = tk.Canvas(
        root,
        background='white',
        width=SCALE*SCREEN_WIDTH,
        height=SCALE*SCREEN_HEIGHT
    )
    canvas.pack()

    game = SnakeGame(canvas)

    for direction in DIRECTIONS:
        root.bind(f'<{direction}>', game.set_direction)

    root.mainloop()


if __name__ == '__main__':
    main()