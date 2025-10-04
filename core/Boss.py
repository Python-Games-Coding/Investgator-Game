from PIL import Image, ImageTk
import tkinter as tk
import os

class Boss:
    def __init__(self, parent, boss_name, x=100, y=765):
        self.parent = parent
        self.boss_name = boss_name
        self.x = x
        self.y = y
        self.label = tk.Label(parent)
        self.image_path = f"textures/boss/{self.boss_name}/stick-L1.gif"
        self.direction = "L"
        self.current_frame = 0
        self.animating = False
        self.frames = [f"stick-L1.gif", f"stick-L2.gif", f"stick-L3.gif"]
        self.load_image()
        self.label.place(x=self.x, y=self.y)

    def load_image(self):
        path = f"textures/boss/{self.boss_name}/{self.frames[self.current_frame]}"
        if not os.path.exists(path):
            img = Image.new("RGBA", (50, 50), (255, 0, 0, 0))
        else:
            img = Image.open(path)
        photo = ImageTk.PhotoImage(img)
        self.label.config(image=photo)
        self.label.image = photo

    def move_to(self, x, y, direction="L"):
        self.x = x
        self.y = y
        self.direction = direction
        self.label.place(x=self.x, y=self.y)
        self.play_animation(direction)

    def play_animation(self, direction):
        self.frames = [f"stick-{direction}1.gif", f"stick-{direction}2.gif", f"stick-{direction}3.gif"]
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.load_image()
        # 只在移动时切换帧，不需要递归after