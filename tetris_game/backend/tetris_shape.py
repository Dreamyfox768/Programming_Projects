import turtle as tt
from random import randint as r
from itertools import cycle
from tetro_base import Tetromino

LJSZT_Offsets = ((0, 1, 0, 0),
                 (1, 0, 0, 0),
                 (0, 0, 0, -1),
                 (0, 0, -1, 0))


class O(Tetromino):
    rot_offsets = ((1, 1, -1, 0), ) * 4

    def draw(self, x, y, color="yellow"):
        self.start = (x, y)
        self.cells.clear()
        self.pen.clear()
        for _ in range(2):
            for _ in range(2):
                super().draw(x, y, color)
                x += self.size
            y -= self.size
            x -= self.size * 2
        self.update_bounds()

    def update_bounds(self):
        x, y = self.start
        s = self.size
        self.rot_bounds = x-s, y-s*3, x+s*3, y
        self.rot_center = x+s, y-s


class I(Tetromino):
    rot_offsets = (0, 2, 0, -1), (2, 0, -1, 0), (0, 1, 0, -2), (1, 0, -2, 0)

    def draw(self, x, y, color="lightblue"):
        self.start = (x, y)
        self.cells.clear()
        self.pen.clear()
        for _ in range(4):
            super().draw(x, y, color)
            x += self.size
        self.update_bounds()

    def update_bounds(self):
        x, y = self.start
        s = self.size
        self.rot_bounds = xl, yl, xh, yh = x, y-s*3, x+s*4, y+s
        self.rot_center = (xl+xh)/2, (yl+yh)/2


class Z(Tetromino):
    rot_offsets = LJSZT_Offsets

    def draw(self, x, y, color="red"):
        self.start = (x, y)
        self.cells.clear()
        self.pen.clear()
        for _ in range(2):
            for _ in range(2):
                super().draw(x, y, color)
                x += self.size
            y -= self.size
            x -= self.size
        self.update_bounds()

    def update_bounds(self):
        x, y = self.start
        s = self.size
        self.rot_bounds = xl, yl, xh, yh = x, y-s*3, x+s*3, y
        self.rot_center = (xl+xh)/2, (yl+yh)/2


class S(Tetromino):
    rot_offsets = LJSZT_Offsets

    def draw(self, x, y, color="green"):
        self.start = (x, y)
        self.cells.clear()
        self.pen.clear()
        for _ in range(2):
            for _ in range(2):
                super().draw(x, y, color)
                x += self.size
            y -= self.size
            x -= self.size * 3
        self.update_bounds()

    def update_bounds(self):
        x, y = self.start
        s = self.size
        self.rot_bounds = xl, yl, xh, yh = x-s, y-s*3, x+s*2, y
        self.rot_center = (xl+xh)/2, (yl+yh)/2


class T(Tetromino):
    rot_offsets = LJSZT_Offsets

    def draw(self, x, y, color="purple"):
        self.start = (x, y)
        self.cells.clear()
        self.pen.clear()
        super().draw(x, y, color)
        x -= self.size
        y -= self.size
        for _ in range(3):
            super().draw(x, y, color)
            x += self.size
        self.update_bounds()

    def update_bounds(self):
        x, y = self.start
        s = self.size
        self.rot_bounds = xl, yl, xh, yh = x-s, y-s*3, x+s*2, y
        self.rot_center = (xl+xh)/2, (yl+yh)/2


class L(Tetromino):
    rot_offsets = LJSZT_Offsets

    def draw(self, x, y, color="orange"):
        self.start = (x, y)
        self.cells.clear()
        self.pen.clear()
        super().draw(x, y, color)
        x -= self.size * 2
        y -= self.size
        for _ in range(3):
            super().draw(x, y, color)
            x += self.size
        self.update_bounds()

    def update_bounds(self):
        x, y = self.start
        s = self.size
        self.rot_bounds = xl, yl, xh, yh = x-s*2, y-s*3, x+s, y
        self.rot_center = (xl + xh)/2, (yl + yh)/2


class J(Tetromino):
    rot_offsets = LJSZT_Offsets

    def draw(self, x, y, color="blue"):
        self.start = (x, y)
        self.cells.clear()
        self.pen.clear()
        super().draw(x, y, color)
        y -= self.size
        for _ in range(3):
            super().draw(x, y, color)
            x += self.size
        self.update_bounds()

    def update_bounds(self):
        x, y = self.start
        s = self.size
        self.rot_bounds = xl, yl, xh, yh = x, y-s*3, x+s*3, y
        self.rot_center = (xl + xh)/2, (yl + yh)/2


def change_tetro(x, y):
    global shapes, tetro
    if tetro:
        tetro.pen.clear()
    tetro = next(shapes)(100)
    tetro.draw(-tetro.size, tetro.size, f"#{r(0, 255):02x}{r(0, 255):02x}{r(0, 255):02x}")
    tetro.draw_bounds()
    print(*tetro.cells, sep="\n")
    print()
    tt.update()


def move_tetro(key):
    global tetro
    key = "rotate" if key == "space" else key
    getattr(tetro, key.lower())()
    tetro.draw_bounds()


if __name__ == '__main__':
    tt.tracer(100)
    tt.ht()

    tetro = Tetromino()
    shapes = cycle((O, Z, S, J, L, T, I))

    screen = tt.getscreen()
    screen.onclick(change_tetro)
    for move in "Left Right Up Down space".split():
        screen.onkey(lambda k=move: move_tetro(k), move)
    screen.listen()

    tt.mainloop()
