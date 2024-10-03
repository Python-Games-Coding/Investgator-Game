import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence

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
        # 添加提示信息标签
        label = tk.Label(self, text="Please Select A Character", font=("Arial", 14))
        label.grid(row=0, columnspan=5, pady=10)
        a = 1
        text = 'Daryl'
        for i in range(5):
            img = Image.open(f"Characters/character_{i+1}.png")  # 更新图片路径
            self.images.append(img)  # 保存原始图片
            photo = ImageTk.PhotoImage(img.resize((50, 50), Image.LANCZOS))
            btn = tk.Button(self, image=photo, command=lambda i=i: self.select_character(i))
            btn.image = photo  # Keep a reference to avoid garbage collection
            btn.grid(row=1, column=i, padx=10, pady=10, sticky="nsew")
            self.buttons.append(btn)
            if a == 1:
                text = 'Daryl'
            elif a == 2:
                text = 'Mango'
            elif a == 3:
                text = 'Brash'
            elif a == 4:
                text = 'Cilantro'
            elif a == 5:
                text = 'RoboBrash'

            # 在按钮上添加文字
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
            # 计算新的宽度和高度，保持图片比例
            img = self.images[i]
            aspect_ratio = img.width / img.height
            new_width = max(min(event.width // 5, event.height // 3) - 20, 150)  # 设置最小宽度为 150
            new_height = int(new_width / aspect_ratio)
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_img)
            btn.config(image=photo)
            btn.image = photo  # Keep a reference to avoid garbage collection

    def select_character(self, index):
        for i, btn in enumerate(self.buttons):
            if i == index:
                btn.config(state="disabled", highlightbackground="green", highlightthickness=2)
            else:
                btn.config(state="normal", highlightbackground="black", highlightthickness=0)
        ind = index + 1
        if ind == 1:
            self.player = 'Daryl'
        elif ind == 2:
            self.player = 'Mango'
        elif ind == 3:
            self.player = 'Brash'
        elif ind == 4:
            self.player = 'Cilantro'
        elif ind == 5:
            self.player = 'RoboBrash'
        
        self.unbind("<Configure>")  # 解除绑定以防止在销毁按钮后调用 resize_images

    def show_loading_screen(self):
        # 清除当前窗口内容
        for widget in self.winfo_children():
            widget.destroy()

        # 设置背景颜色为红色
        self.configure(bg='red')

        # 加载并显示 GIF
        gif_path = "ProgressBar/ProgressBar.gif"
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
                self.after(1, self.show_blank_window)  # 5秒后显示空白页面

        update_frame(0)

        # 显示 "Loading..."
        loading_label = tk.Label(self, text="Loading...", font=("Arial", 16), bg='red', fg='white')
        loading_label.pack(pady=20)

    def confirm_selection(self):
        if self.player is not None:
            self.show_loading_screen()
        else:
            messagebox.showwarning("Character Selection", "Please select a character")

    def show_blank_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg='SystemButtonFace')  # 恢复默认背景颜色
        self.title("Game")

if __name__ == "__main__":
    app = CharacterSelection()
    app.mainloop()