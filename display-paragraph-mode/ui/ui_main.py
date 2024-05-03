import customtkinter as ctk
from .text_label import TextLabel
from .input_textbox import InputTextbox
from .speed_label import SpeedLabel
from .reset_button import ResetButton

ctk.set_default_color_theme("green")

class GUI(ctk.CTkFrame):
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.root.title("Speed Typing TestApp")
        self.root.geometry("1000x800")

        bg_color = self.root.cget("bg")
        self.frame = ctk.CTkFrame(self.root, fg_color=bg_color)

        self.create_widgets()

    def run(self):
        self.frame.pack(expand=True)
        self.root.mainloop()

    def create_widgets(self):
        self.text_label = TextLabel().create_text_label(self.frame)
        self.input_textbox = InputTextbox().create_input_textbox(self.frame)
        self. speed_label = SpeedLabel().create_speed_label(self.frame)
        self.reset_button = ResetButton().create_reset_button(self.frame)


