import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
from random import randint
import os

global player_died, health, boss_health, boss_died, little_boss_health, little_boss_died, level, level_complete
player_died = False
health = 350
boss_health = 1000
boss_died = False
little_boss_health = 300
little_boss_died = False
level = 1
level_complete = False

class CharacterSelection(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game")
        self.geometry("1000x750")
        self.player = None
        self.buttons = []
        self.images = []
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Please Select A Character", font=("Arial", 14))
        label.grid(row=0, columnspan=5, pady=10)
        a = 1
        text = 'Marsha'
        for i in range(6):
            img = Image.open(f"textures/characters/character_{i+1}.png")
            self.images.append(img)
            photo = ImageTk.PhotoImage(img.resize((50, 50), Image.LANCZOS))
            btn = tk.Button(self, image=photo, command=lambda i=i: self.select_character(i))
            btn.image = photo
            btn.grid(row=1, column=i, padx=10, pady=10, sticky="nsew")
            self.buttons.append(btn)
            if a == 1:
                text = 'Marsha'
            elif a == 2:
                text = 'Mango'
            elif a == 3:
                text = 'Brash'
            elif a == 4:
                text = 'Cilantro'
            elif a == 5:
                text = 'RoboBrash'
            elif a == 6:
                text = 'Bongo'

            text_label = tk.Label(self, text=text, bg="white")
            text_label.grid(row=1, column=i, padx=10, pady=10, sticky="s")
            a += 1

        self.ok_button = tk.Button(self, text="OK", command=self.confirm_selection)
        self.ok_button.grid(row=2, columnspan=5, pady=20, sticky="nsew")

        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.bind("<Configure>", self.resize_images)

    def resize_images(self, event):
        for i, btn in enumerate(self.buttons):
            if not btn.winfo_exists():
                continue
            img = self.images[i]
            aspect_ratio = img.width / img.height
            new_width = max(min(event.width // 5, event.height // 3) - 20, 150)
            new_height = int(new_width / aspect_ratio)
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_img)
            btn.config(image=photo)
            btn.image = photo

    def select_character(self, index):
        for i, btn in enumerate(self.buttons):
            if i == index:
                btn.config(state="disabled", highlightbackground="green", highlightthickness=2)
            else:
                btn.config(state="normal", highlightbackground="black", highlightthickness=0)
        ind = index + 1
        if ind == 1:
            self.player = 'Marsha'
        elif ind == 2:
            self.player = 'Mango'
        elif ind == 3:
            self.player = 'Brash'
        elif ind == 4:
            self.player = 'Cilantro'
        elif ind == 5:
            self.player = 'RoboBrash'
        elif ind == 6:
            self.player = 'Bongo'
        
        self.unbind("<Configure>")

    def show_loading_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='gray')

        gif_path = "textures/gui/ProgressBar.gif"
        gif = Image.open(gif_path)
        frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

        label = tk.Label(self, bg='red')
        label.pack(expand=True)

        def update_frame(index):
            frame = frames[index]
            label.config(image=frame)
            index = (index + 1) % len(frames)
            if index != 0:
                self.after(100, update_frame, index)
            else:
                self.after(1, self.show_blank_window3)

        update_frame(0)

        loading_label = tk.Label(self, text="Loading...", font=("Arial", 16), bg='red', fg='white')
        loading_label2 = tk.Label(self, text="All for one and ALL-igator!", font=("Arial", 16), bg='red', fg='white')
        loading_label.pack(pady=20)
        loading_label2.pack(pady=20)

    def confirm_selection(self):
        if self.player is not None:
            self.show_loading_screen()
        else:
            messagebox.showwarning("Character Selection", "Please select a character")

    def show_blank_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='SystemButtonFace')
        self.title("Game")

    def start_game(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='green')
        self.title("Creating Game")

        creating_label = tk.Label(self, text="Creating Game", font=("Arial", 16), bg='green', fg='white')
        creating_label.pack(pady=20)

        self.after(randint(1000, 7000), self.show_there_we_go)

    def show_there_we_go(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='green')
        self.title("There We Go!")

        there_we_go_label = tk.Label(self, text="There We Go!", font=("Arial", 16), bg='green', fg='white')
        there_we_go_label.pack(pady=20)

        self.after(500, self.show_blank_window2)

    def show_blank_window2(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='SystemButtonFace')
        self.title("Game")

        self.health_label = tk.Label(self)
        self.health_label.place(x=10, y=10)

        self.update_health_image()

    def update_health_image(self):
        global health
        health_image_path = f"textures/gui/health{health // 50}.png"
    
        if health <= 0:
            self.respawn()
            return

        health_img = Image.open(health_image_path)
        health_photo = ImageTk.PhotoImage(health_img)
        self.health_label.config(image=health_photo)
        self.health_label.image = health_photo

        # 只有在 health 大于 0 时才继续减少
        if health > 0:
            self.after(1000, self.update_health_image)

    def respawn(self):
        global health
        health = 350
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='SystemButtonFace')
        self.title("You Died")
        level_complete_label = tk.Label(self, text="You Died", font=("Arial", 16), bg='SystemButtonFace', fg='Black')
        win_level_button = tk.Button(self, text="Back to Menu", command=self.show_blank_window3)
        go_to_SUIT_button = tk.Button(self, text="Go to S.U.I.T. Headquarters", command=self.show_blank_window4)
        play_again_button = tk.Button(self, text="Play Again", command=self.start_game)
        quit_button = tk.Button(self, text="Quit Game", command=self.quit)
        win_level_button.pack(pady=20)
        go_to_SUIT_button.pack(pady=20)
        play_again_button.pack(pady=20)
        quit_button.pack(pady=20)

    def show_blank_window3(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='SystemButtonFace')
        self.title("Game")
        start_button = tk.Button(self, text="Start Game", command=self.start_game)
        player_label = tk.Label(self, text="Character: " + str(self.player), font=("Arial", 16), bg='SystemButtonFace', fg='black')
        quit_button = tk.Button(self, text="Quit Game", command=self.quit)
        start_button.pack(pady=20)
        player_label.pack(pady=20)
        quit_button.pack(pady=20)

    def show_blank_window4(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='SystemButtonFace')
        self.title("Game")

    def level_complete(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='Green')
        self.title("Game")
        global level
        if int(level) < 8:
            level_complete_label = tk.Label(self, text="Level Complete", font=("Arial", 16), bg='Green', fg='White')
            level_complete_label.pack(pady=20)
            next_level_button = tk.Button(self, text="Next Level", command=self.start_game)
            go_to_SUIT_button = tk.Button(self, text="Go to S.U.I.T. Headquarters", command=self.show_blank_window4)
            next_level_button.pack(pady=20)
            go_to_SUIT_button.pack(pady=20)
            level += 1
        else:
            level_complete_label = tk.Label(self, text="Congratulations! You have completed the game!\nPlease Choose A Option Below", font=("Arial", 16), bg='Green', fg='White')
            level_complete_label.pack(pady=20)
            win_level_button = tk.Button(self, text="Back to Menu", command=self.show_blank_window3)
            go_to_SUIT_button = tk.Button(self, text="Go to S.U.I.T. Headquarters", command=self.show_blank_window4)
            play_again_button = tk.Button(self, text="Play Again", command=self.start_game)
            quit_button = tk.Button(self, text="Quit Game", command=self.quit)
            win_level_button.pack(pady=20)
            go_to_SUIT_button.pack(pady=20)
            play_again_button.pack(pady=20)
            quit_button.pack(pady=20)

if __name__ == "__main__":
    app = CharacterSelection()
    app.mainloop()