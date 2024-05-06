import customtkinter as ctk
from .text_label import TextLabel
from .input_textbox import InputTextbox
from .speed_label import SpeedLabel
from .reset_button import ResetButton

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("Dark")


class GUI(ctk.CTkFrame):
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.root.title("TypeMaster")
        self.root.geometry("1000x800")

        bg_color = self.root.cget("bg")
        self.frame = ctk.CTkFrame(self.root, fg_color=bg_color)

        self.create_widgets()

    def run(self):
        self.frame.pack(expand=True)
        self.root.mainloop()

    def create_widgets(self):
        self.text_label = TextLabel(self.frame)
        self.input_textbox = InputTextbox(self.frame)
        self.speed_label = SpeedLabel(self.frame)
        self.reset_button = ResetButton(self.frame)
