import tkinter as tk
from tkinter import ttk
import turtle
from tetris.sys230.Turtle2 import World  # Assuming your World class is in main.py


class TetrisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TETRIS-CX")
        self.geometry("900x700")
        self.resizable(False, False)

        self.create_widgets()
        self.setup_turtle_canvas()

    def create_widgets(self):
        control_frame = tk.Frame(self, width=120, bg="#f0f0f0")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(control_frame, text="TETRIS-CX", font=("Arial", 14, "bold")).pack(pady=10)
        self.level_label = tk.Label(control_frame, text="level++ >> 1", font=("Arial", 10))
        self.level_label.pack(pady=5)

        tk.Button(control_frame, text="▶ Play", command=self.play).pack(pady=5)
        tk.Button(control_frame, text="⏸ Pause", command=self.pause).pack(pady=5)
        tk.Button(control_frame, text="⏹ Stop", command=self.stop).pack(pady=5)

        status_frame = tk.Frame(self, width=180, bg="#e0f7fa")
        status_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.score_label = tk.Label(status_frame, text="Score: 0", font=("Arial", 12))
        self.score_label.pack(pady=10)
        self.lines_label = tk.Label(status_frame, text="Lines: 0", font=("Arial", 12))
        self.lines_label.pack(pady=5)

    def setup_turtle_canvas(self):
        canvas_frame = tk.Frame(self, bg="white")
        canvas_frame.pack(expand=True, fill=tk.BOTH)
        self.canvas = tk.Canvas(canvas_frame, width=600, height=600)
        self.canvas.pack()
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.tracer(0)
        self.world = World(size=30, screen=self.screen)

        # Optional: key controls similar to your code
        self.screen.onkey(lambda: self.world.move("left"), "Left")
        self.screen.onkey(lambda: self.world.move("right"), "Right")
        self.screen.onkey(lambda: self.world.move("down"), "Down")
        self.screen.onkey(lambda: self.world.move("rotate"), "Up")
        self.screen.onkey(lambda: self.world.hard_drop(), "space")
        self.screen.listen()

    def play(self):
        self.world.play()

    def pause(self):
        self.world.pause()

    def stop(self):
        self.world.stop()
        # Reset UI indicators if you track score/lines here

if __name__ == "__main__":
    app = TetrisApp()
    app.mainloop()
