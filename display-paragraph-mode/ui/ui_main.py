import random
import customtkinter as ctk


ctk.set_default_color_theme("green")


class GUI(ctk.CTkFrame):
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.root.title("Speed Typing TestApp")
        self.root.geometry("1000x800")

        self.text_data = open("text_data.txt", "r").read().split("\n")

        bg_color = self.root.cget("bg")
        self.frame = ctk.CTkFrame(self.root, fg_color=bg_color)

        self.create_text_label()
        self.create_input_entry()
        self.create_speed_label()
        self.create_reset_button()

    def run(self):
        self.frame.pack(expand=True)
        self.root.mainloop()

    def create_text_label(self):
        text = random.choice(self.text_data)
        label = ctk.CTkLabel(
            self.frame,
            text=text,
            font=("Cascadia Code", 16),
            wraplength=600,
            height=200,
            justify='left',
            fg_color=("grey18"),
            corner_radius=8
        )
        label.grid(row=0, column=0, columnspan=2,
                   padx=100, pady=[100, 0], ipady=50, ipadx=50)
        self.text_label = label

    def create_input_entry(self):
        input_entry = ctk.CTkEntry(
            self.frame,
            width=600,
            height=50,
            font=("Cascadia Code", 16)
        )
        input_entry.grid(row=1, column=0, columnspan=2,
                         pady=50)
        self.input_entry = input_entry

    def create_speed_label(self):
        speed_label = ctk.CTkLabel(
            self.frame,
            text="Speed: \n0.00 CPS\n0.00 CPM",
            font=("Ubuntu", 16),
            fg_color="lightblue",
            text_color="black",
            corner_radius=8,
            justify="left"
        )
        speed_label.grid(row=2, column=0, columnspan=1, ipadx=20, ipady=20)
        self.speed_label = speed_label

    def create_reset_button(self):
        reset_button = ctk.CTkButton(
            self.frame,
            text="Reset",
            font=("Ubuntu", 16),
            text_color="black",
            height=50
        )
        reset_button.grid(row=2, column=1, columnspan=1)
        self.reset_button = reset_button
