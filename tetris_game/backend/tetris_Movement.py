import turtle as tt
from collections.abc import Sequence
from random import randint
from math import sin, cos, pi


class Cell:
    def __init__(self, size, color, pen, *points, state=0):
        assert len(points) == 4, "Number of points must be 4"
        assert points[0] != points[1] != points[2] != points[3], "There can't be duplicates in cell corners"
        self.points = list(points)
        self.color = color
        self.pen = pen
        self.size = size
        self.state = state

    def draw(self):
        self.pen.pu()
        self.pen.goto(self.points[0])
        self.pen.fillcolor(self.color)
        self.pen.pd()
        self.pen.begin_fill()
        for p in self.points + [self.points[0]]:
            self.pen.goto(p)
        self.pen.end_fill()

    def rotate(self, xc, yc):
        self.points = [( round(xc + (x-xc)*cos(-pi/2) - (y-yc)*sin(-pi/2)),
                         round(yc + (x-xc)*sin(-pi/2) + (y-yc)*cos(-pi/2)) )
                            for x, y in self.points]

    def translate_x(self, factor=1):
        self.points = [(x+factor*self.size, y) for x, y in self.points]

    def translate_y(self, factor=1):
        self.points = [(x, y+factor*self.size) for x, y in self.points]

    def get_bounds(self):
        xl, xh = sorted(set(x for x, y in self.points))
        yl, yh = sorted(set(y for x, y in self.points))
        return xl, yl, xh, yh

    def __neg__(self):
        points = [(x, y-self.size) for x, y in self.points]
        s, c, p = self.size, self.color, self.pen
        return Cell(s, c, p, *points)

    def __rshift__(self, factor:int):
        points = [(x+factor*self.size, y) for x, y in self.points]
        s, c, p = self.size, self.color, self.pen
        return Cell(s, c, p, *points)

    def __lshift__(self, factor:int):
        points = [(x-factor*self.size, y) for x, y in self.points]
        s, c, p = self.size, self.color, self.pen
        return Cell(s, c, p, *points)

    def __mul__(self, point: Sequence[float, float]):
        xc, yc = point
        points = [(round(xc + (x-xc) * cos(-pi/2) - (y - yc) * sin(-pi/2)),
                   round(yc + (x-xc) * sin(-pi/2) + (y - yc) * cos(-pi/2)))
                  for x, y in self.points]
        s, c, p = self.size, self.color, self.pen
        return Cell(s, c, p, *points)

    def __eq__(self, other):
        if not isinstance(other, Cell): return NotImplemented
        return set(self.points) == set(other.points)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f"{self.__class__.__name__}{self.get_bounds()}"

    def __repr__(self):
        return str(self)


class Tetromino:
    rot_offsets = ((0, 0, 0, 0), ) * 4

    def __init__(self, size=20, screen=None):
        self.__size = size
        self.start = None
        self.rot_center = (0, 0)
        self.rot_bounds = None
        self.color = "white"
        self.cells = []
        self.state = 0
        self.pen = tt.RawTurtle(screen or tt.getscreen(), visible=False)

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    def draw(self, x, y, color=""):
        self.start = self.start or (x, y)
        self.color = color or self.color
        self.pen.pu()
        self.pen.goto(x, y)
        self.pen.fillcolor(self.color)
        self.pen.pd()
        self.pen.begin_fill()
        points = []
        for _ in range(4):
            self.pen.fd(self.size)
            self.pen.right(90)
            x, y = [round(p) for p in self.pen.pos()]
            points.append((x,y))
        self.cells.append(Cell(self.size, color, self.pen, *points))
        self.pen.end_fill()

    def draw_bounds(self):
        if self.rot_bounds:
            xl, yl, xh, yh = self.rot_bounds
            points = [(xl, yl), (xl, yh), (xh, yh), (xh, yl)]
            self.pen.pu()
            self.pen.goto(points[0])
            self.pen.pd()
            for p in points + [points[0]]:
                self.pen.goto(p)
            self.update_screen()

    def redraw(self):
        self.pen.clear()
        self.update_bounds()
        for cell in self.cells:
            cell.draw()
        self.update_screen()

    def right(self, factor:int=1):
        if self.cells:
            x, y = self.start
            self.start = x + factor * self.size, y
            self.update_bounds()
            for cell in self.cells:
                cell.translate_x(factor)
            self.redraw()

    def left(self, factor:int=1):
        self.right(-factor)

    def up(self, factor:int=1):
        x, y = self.start
        self.start = x, y + factor*self.size
        for cell in self.cells:
            cell.translate_y(factor)
        self.redraw()

    def down(self, factor:int=1):
        self.up(-factor)

    def rotate(self):
        for c in self.cells:
            c.rotate(*self.rot_center)
        self.redraw()
        self.change_state()

    def check_overlap(self, *cells: Cell, other:"Tetromino"=None):
        cells = other.cells if other else cells
        for other_cell in cells:
            for my_cell in self.cells:
                if other_cell == my_cell:
                    return True
        return False

    def change_state(self):
        self.state = (self.state + 1) % 4

    def get_actual_bounds(self, state: int=None):
        if self.rot_bounds:
            offsets = self.rot_offsets[state or self.state]
            bounds = self.rot_bounds
            return [l+o*self.size for l, o in zip(bounds, offsets)]

    def update_bounds(self):
        self.rot_center = (0, 0)

    def clear(self):
        self.pen.clear()

    def update_screen(self):
        self.pen.getscreen().update()


def draw(x, y):
    r, g, b = [randint(0, 255) for _ in range(3)]
    colr = f"#{r:02x}{g:02x}{b:02x}"
    tetro.draw(x, y, colr)


def move_tetro(key):
    global tetro
    key = "rotate" if key == "space" else key
    getattr(tetro, key.lower())()
    tetro.draw_bounds()


if __name__ == '__main__':
    tt.tracer(100)
    tt.ht()

    tetro = Tetromino()

    screen = tt.getscreen()
    screen.onclick(draw)
    for move in "Left Right Up Down space".split():
        screen.onkey(lambda k=move: move_tetro(k), move)
    screen.listen()

    tt.mainloop()
