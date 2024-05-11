import customtkinter as ctk
from input_textbox import InputTextbox
from reset_button import ResetButton
from words_label import WordsLabel

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("Dark")

class GUI(ctk.CTkFrame):
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.root.title("TypeMaster")
        self.root.geometry("1200x900")

        bg_color = self.root.cget("bg")
        self.frame = ctk.CTkFrame(self.root, fg_color=bg_color)

    def run(self):
        self.frame.pack(expand=True)
        self.root.mainloop()

    def create_widgets(self):
        self.input_textbox = InputTextbox(self.frame)
        self.words_label = WordsLabel(self.frame)
        self.reset_button = ResetButton(self.frame)






