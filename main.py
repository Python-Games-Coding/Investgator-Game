import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
from random import randint
import os

from core import log, verables, SimpleButton
from core.Boss import Boss
from core.BossAI import BossAI
from core.player import Player

class InvestgatorsGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game")
        self.geometry("1300x800")
        self.player = None
        self.buttons = []
        self.images = []
        self.create_widgets()
        self.boss_name = self.get_boss_name()
        log.PrintLn('Game Start', moudle="Core")

    def get_boss_name(self):
        level = verables.level
        boss_names = {
            1: 'howdino',
            2: 'Crackerdile',
            3: 'Waffledile',
            4: 'Dong',
            5: 'Rocodile',
            6: 'Savana',
            7: 'Bill-N-Dollaz',
            8: 'Phillip'
        }
        return boss_names.get(level, 'howdino')

    def create_widgets(self):
        label = tk.Label(self, text="Please Select A Character", font=("Arial", 14))
        label.grid(row=0, columnspan=5, pady=10)
        character_names = ['Marsha', 'Mango', 'Brash', 'Cilantro', 'RoboBrash', 'Bongo']
        for i, name in enumerate(character_names):
            img = Image.open(f"textures/characters/character_{i+1}.png")
            self.images.append(img)
            photo = ImageTk.PhotoImage(img.resize((50, 50), Image.LANCZOS))
            btn = tk.Button(self, image=photo, command=lambda i=i: self.select_character(i))
            btn.image = photo
            btn.grid(row=1, column=i, padx=10, pady=10, sticky="nsew")
            self.buttons.append(btn)
            text_label = tk.Label(self, text=name, bg="white")
            text_label.grid(row=1, column=i, padx=10, pady=10, sticky="s")

        self.ok_button = tk.Button(self, text="OK", command=self.confirm_selection)
        self.ok_button.grid(row=2, columnspan=5, pady=20, sticky="nsew")

        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.resize_job = None  # 新增
        self.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        if hasattr(self, "resize_job") and self.resize_job:
            self.after_cancel(self.resize_job)
        self.resize_job = self.after(100, lambda: self.resize_images(event))

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
        character_names = ['Marsha', 'Mango', 'Brash', 'Cilantro', 'RoboBrash', 'Bongo']
        for i, btn in enumerate(self.buttons):
            if i == index:
                btn.config(state="disabled", highlightbackground="green", highlightthickness=2)
            else:
                btn.config(state="normal", highlightbackground="black", highlightthickness=0)
        self.player = character_names[index]
        self.unbind("<Configure>")

    def confirm_selection(self):
        if self.player is not None:
            self.show_loading_screen()
        else:
            messagebox.showwarning("Character Selection", "Please select a character")

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
                self.after(10, update_frame, index)
            else:
                self.after(1, self.show_blank_window3)
        update_frame(0)

        loading_label = tk.Label(self, text="Loading...", font=("Arial", 16), bg='red', fg='white')
        loading_label2 = tk.Label(self, text="All for one and ALL-igator!", font=("Arial", 16), bg='red', fg='white')
        loading_label.pack(pady=20)
        loading_label2.pack(pady=20)

    def show_blank_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='SystemButtonFace')
        self.title("Game")

    def show_blank_window3(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='SystemButtonFace')
        self.title("Game")
        start_button = tk.Button(self, text="Start Game", command=self.start_game)
        player_label = tk.Label(self, text="Character: " + str(self.player), font=("Arial", 16), bg='SystemButtonFace', fg='black')
        quit_button = tk.Button(self, text="Quit Game", command=self.quit)
        log.PrintLn('Loaded Main Page', moudle="Window")
        start_button.pack(pady=20)
        player_label.pack(pady=20)
        quit_button.pack(pady=20)

    def start_game(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='green')
        self.title("Creating Game")
        creating_label = tk.Label(self, text="Creating Game", font=("Arial", 16), bg='green', fg='white')
        creating_label.pack(pady=20)
        log.PrintLn('Creating game', moudle="Window")
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
        player_name = self.player if self.player else "Unknown"
        log.PrintLn(player_name + ' Joined The Game', moudle="Player")
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='SystemButtonFace')
        self.title("Game")
        self.health_label = tk.Label(self)
        self.health_label.place(x=10, y=10)
        # 不要再创建 self.character_label
        # self.character_label = tk.Label(self)
        # self.character_label.place(x=50, y=300)
        # 只创建 Player
        self.player_obj = Player(self, self.player, x=50, y=300)
        self.bind("<KeyPress>", self.player_obj.on_key_press)
        self.bind("<KeyRelease>", self.player_obj.on_key_release)
        self.player_obj.update_gravity()
        self.player_obj.update_movement()
        self.after(randint(1000, 5000), self.show_boss)

    def show_boss(self):
        self.boss = Boss(self, self.boss_name, x=randint(20, 1100), y=765)
        self.boss_ai = BossAI(self.boss, self)
        log.PrintLn("Loaded Boss " + self.boss_name, moudle="Boss")
        self.after(randint(1000, 5000), self.boss_ai.start_random_move)
        log.PrintLn("Loaded AI " + self.boss_name, moudle="Boss")

    def respawn(self):
        verables.health = 350
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
        if int(verables.level) < 8:
            level_complete_label = tk.Label(self, text="Level Complete", font=("Arial", 16), bg='Green', fg='White')
            level_complete_label.pack(pady=20)
            next_level_button = tk.Button(self, text="Next Level", command=self.start_game)
            go_to_SUIT_button = tk.Button(self, text="Go to S.U.I.T. Headquarters", command=self.show_blank_window4)
            next_level_button.pack(pady=20)
            go_to_SUIT_button.pack(pady=20)
            verables.level += 1
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

    def update_health_image(self):
        health_image_path = f"textures/gui/health{verables.health // 50}.png"
        if verables.health <= 0:
            self.respawn()
            return
        health_img = Image.open(health_image_path)
        health_photo = ImageTk.PhotoImage(health_img)
        self.health_label.config(image=health_photo)
        self.health_label.image = health_photo
        if verables.health > 0:
            self.after(1000, self.update_health_image)

if __name__ == "__main__":
    app = InvestgatorsGame()
    app.mainloop()
