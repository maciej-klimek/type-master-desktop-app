import random
import customtkinter as ctk

ctk.set_default_color_theme("green")


class GUI(ctk.CTkFrame):
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.root.title("Speed Typing TestApp")
        self.root.geometry("1000x800")

        # self.text_data = open("text_data.txt", "r").read().split("\n")

        bg_color = self.root.cget("bg")
        self.frame = ctk.CTkFrame(self.root, fg_color=bg_color)

        self.create_text_label()
        self.create_input_textbox()
        self.create_speed_label()
        self.create_reset_button()

    def run(self):
        self.frame.pack(expand=True)
        self.root.mainloop()

    def create_text_label(self):
        # text = random.choice(self.text_data)
        label = ctk.CTkLabel(
            self.frame,
            # text="Kliknij mnie żeby zacząć",
            font=("Cascadia Code", 16),
            wraplength=600,
            justify='left',
            fg_color=("grey18"),
            corner_radius=8,
        )
        label.pack(fill="both", expand=True, ipady=50, ipadx=50)
        self.text_label = label

    def create_input_textbox(self):
        input_textbox = ctk.CTkTextbox(
            self.frame,
            fg_color=("grey18"),
            width=600,
            height=60,
            font=("Cascadia Code", 16),
            border_color="grey30",
            border_width=2,
            wrap="word"
        )
        input_textbox.pack(expand=True, pady=50, padx=50)
        self.input_textbox = input_textbox

    def create_speed_label(self):
        speed_label = ctk.CTkLabel(
            self.frame,
            text="Accuracy: 0% \nCPS: 0\nCPM: 0",
            font=("Ubuntu", 16),
            corner_radius=8,
            justify="left",
            fg_color="#71c788",
            text_color="black",

        )
        speed_label.pack(side="left", padx=[50, 0], ipadx=20, ipady=20)
        self.speed_label = speed_label

    def create_reset_button(self):
        reset_button = ctk.CTkButton(
            self.frame,
            height=40,
            text="Reset",
            font=("Ubuntu", 16),
            fg_color="grey18",
            text_color="white",
            border_color="grey30",
            border_width=2,
            hover_color="grey30"
        )
        reset_button.pack(side="right", padx=[0, 50])
        self.reset_button = reset_button
