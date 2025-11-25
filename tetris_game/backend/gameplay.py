import turtle as tt
from itertools import cycle
from tetris_shape import I, J, L, S, Z, O, T
from tetris_Movement import Tetromino, Cell

SHAPE_CLASSES = cycle((I, J, L, S, Z, O, T))

class World(Tetromino):
    """Represents the tetris world defined by a grid of 20x10 (visible) cells"""

    def __init__(self, size=20, screen=None):
        super().__init__(size, screen)
        self.screen = self.pen.getscreen()
        self.stack = Stack(self)
        self.tetro = None
        self.running = False        # NEW: gate the game loop
        self.tick_ms = 400          # NEW: loop interval
        self.init_screen()

    def init_screen(self, **settings):
        s = self.size
        x1, y1, xu, yu = -5, 0, 15, 20
        self.screen.setworldcoordinates(x1 * s, y1 * s, xu * s, yu * s)
        self.screen.bgcolor("#C6DEF1")
        self.draw(0, s, "#FAEDCB")
        self.spawn()

    def draw(self, x, y, color=""):
        """Draws the world, a 20x10 grid"""
        for row in range(20):
            for col in range(10):
                super().draw(x, y, color)
                x += self.size
            x, y = 0, y + self.size
        self.screen.update()

    def spawn(self):
        """create a new/active tetro"""
        self.tetro = next(SHAPE_CLASSES)(self.size, self.screen)
        x, y = 4 * self.size, 22 * self.size
        self.tetro.draw(x, y)
        self.screen.update()

    def move(self, instr="down"):
        if any(self.stack.state_matrix[19]):
            self.game_over()
            return

        temp_cells = []
        for cell in self.tetro.cells:
            new_cell = Cell(self.size, cell.color, cell.pen, *cell.points)
            if instr == "down":
                new_cell.translate_y(-1)
            elif instr == "left":
                new_cell.translate_x(-1)
            elif instr == "right":
                new_cell.translate_x(1)
            elif instr == "rotate":
                new_cell = new_cell * self.tetro.rot_center

            temp_cells.append(new_cell)

        if self.stack.ok_move(temp_cells, self.tetro):
            getattr(self.tetro, instr)()
        else:
            if instr == "down":
                self.stack.absorb(*self.tetro.cells, tetro=self.tetro)
                self.stack.request_tetro()

        self.tetro.draw_bounds()

    def hard_drop(self):
        """While ok drop current tetro by a cell"""
        while True:
            temp_cells = []
            for cell in self.tetro.cells:
                new_cell = Cell(self.size, cell.color, cell.pen, *cell.points)
                new_cell.translate_y(-1)
                temp_cells.append(new_cell)

            if self.stack.ok_move(temp_cells, self.tetro):
                self.tetro.down()
            else:
                self.stack.absorb(*self.tetro.cells, tetro=self.tetro)
                self.stack.request_tetro()
                break

        self.screen.update()

    # ---------- NEW: controlled game loop ----------
    def play(self):
        """Start or resume the game loop."""
        if self.running:
            return
        self.running = True
        self.screen.ontimer(self.tick, self.tick_ms)

    def pause(self):
        """Pause the game loop."""
        self.running = False
        # No timer cancel in turtle; gating via `running` stops re-scheduling.

    def stop(self):
        """Stop the game and reset world and stack."""
        self.running = False
        self.pen.clear()
        self.stack.cells.clear()
        self.stack.init_state_matrix()
        self.tetro = None
        self.init_screen()

    def tick(self):
        """One loop iteration. Reschedules only if running."""
        if not self.running:
            return
        # Advance game one step
        self.move("down")
        # Schedule next tick
        self.screen.ontimer(self.tick, self.tick_ms)
    # ---------- END NEW ----------

    def game_over(self):
        self.pause()
        self.pen.penup()
        self.pen.goto(5 * self.size, 10 * self.size)
        self.pen.color("white")
        self.pen.write("GAME OVER!", align="center", font=("Arial", 40, "bold"))
        self.screen.update()
        print("Game Over!")

    def update_score(self, lines):
        if lines:
            print(f"Cleared {lines} lines")


class Stack(Tetromino):
    def __init__(self, world: World):
        super().__init__(world.size, world.screen)
        self.state_matrix = None
        self.world = world
        self.cells = []
        self.init_state_matrix()

    def init_state_matrix(self):
        self.state_matrix = [[0 for _ in range(10)] for _ in range(20)]

    def ok_move(self, cells: list[Cell], tetro: Tetromino, move="down") -> bool:
        for cell in cells:
            xl, yl, xh, yh = cell.get_bounds()
            if xl < 0 or xh > self.size * 10 or yl < 0:
                return False
            for my_cell in self.cells:
                mx, my, _, _ = my_cell.get_bounds()
                if xl == mx and yl == my:
                    return False
        return True

    def absorb(self, *cells, tetro: Tetromino = None):
        for cell in cells:
            xl, yl, _, _ = cell.get_bounds()
            row = int(yl // self.size)
            col = int(xl // self.size)
            if 0 <= row < 20 and 0 <= col < 10:
                self.state_matrix[row][col] = 1
                self.cells.append(cell)

        cleared = self.rearrange()
        self.world.update_score(cleared)
        self.redraw()

    def request_tetro(self):
        self.world.spawn()

    def rearrange(self):
        full_rows = [i for i, row in enumerate(self.state_matrix) if all(row)]
        if not full_rows:
            return 0

        # Process from bottom to top
        for r in sorted(full_rows, reverse=True):
            self.state_matrix.pop(r)
            self.state_matrix.insert(0, [0 for _ in range(10)])

        new_cells = []
        for cell in self.cells:
            xl, yl, _, _ = cell.get_bounds()
            row = int(yl // self.size)

            if row in full_rows:
                cell.pen.clear()
                continue

            # Drop by number of cleared rows below
            drop = sum(1 for r in full_rows if r < row)
            if drop > 0:
                cell.translate_y(-drop)

            new_cells.append(cell)

        self.cells = new_cells
        self.pen.clear()
        for cell in self.cells:
            cell.draw()
        self.update_screen()

        return len(full_rows)
