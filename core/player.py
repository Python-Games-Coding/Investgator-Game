import os
import tkinter as tk
from PIL import Image, ImageTk

class Player:
    def __init__(self, parent, player_name, x=50, y=300):
        self.parent = parent
        self.player_name = player_name
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.is_jumping = False
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_animating = False
        self.current_frame = 0

        self.label = tk.Label(self.parent)
        self.label.place(x=self.x, y=self.y)
        self.update_image("L")

    def update_image(self, direction):
        frame = f"stick-{direction}1.gif"
        image_path = f"textures/player/{self.player_name}/{frame}"
        if not os.path.exists(image_path):
            img = Image.new("RGBA", (50, 50), (255, 0, 0, 0))
        else:
            img = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(img)
        self.label.config(image=self.photo)
        self.label.image = self.photo

    def play_animation(self, direction):
        frames = [f"stick-{direction}1.gif", f"stick-{direction}2.gif", f"stick-{direction}3.gif"]
        if not hasattr(self, "current_frame"):
            self.current_frame = 0

        def animate():
            if not (self.is_moving_left if direction == "L" else self.is_moving_right):
                self.is_animating = False
                return
            frame = frames[self.current_frame]
            image_path = f"textures/player/{self.player_name}/{frame}"
            if not os.path.exists(image_path):
                img = Image.new("RGBA", (50, 50), (255, 0, 0, 0))
            else:
                img = Image.open(image_path)
            photo = ImageTk.PhotoImage(img)
            self.label.config(image=photo)
            self.label.image = photo
            max_x = self.parent.winfo_width() - 50
            if direction == "L":
                self.x = max(0, self.x - 9)
            elif direction == "R":
                self.x = min(max_x, self.x + 9)
            self.label.place(x=self.x, y=self.y)
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.parent.after(100, animate)
        animate()

    def update_gravity(self):
        self.velocity_y += 2
        self.y += self.velocity_y
        if self.y >= 765:
            self.y = 765
            self.velocity_y = 0
            self.is_jumping = False
        max_x = self.parent.winfo_width() - 50
        if self.x > max_x:
            self.x = max_x
        elif self.x < 0:
            self.x = 0
        self.label.place(x=self.x, y=self.y)
        self.parent.after(50, self.update_gravity)

    def on_key_press(self, event):
        if event.keysym == "a":
            self.is_moving_left = True
        elif event.keysym == "d":
            self.is_moving_right = True
        elif event.keysym == "space" and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -20

    def on_key_release(self, event):
        if event.keysym == "a":
            self.is_moving_left = False
        elif event.keysym == "d":
            self.is_moving_right = False

    def update_movement(self):
        if not hasattr(self, "is_animating"):
            self.is_animating = False
        if self.is_moving_left and not self.is_animating:
            self.is_animating = True
            self.play_animation("L")
        elif self.is_moving_right and not self.is_animating:
            self.is_animating = True
            self.play_animation("R")
        elif not self.is_moving_left and not self.is_moving_right:
            self.is_animating = False
        self.label.place(x=self.x, y=self.y)
        self.parent.after(50, self.update_movement)