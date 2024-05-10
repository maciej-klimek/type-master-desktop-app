import customtkinter as ctk
from input_textbox import InputTextbox
from reset_button import ResetButton
from words_label import WordsLabel
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

        def creat_widgets(self):
            self.input_textbox = InputTextbox(self.frame)
            self.reset_button = ResetButton(self.frame)
            self.words_label = WordsLabel(self.frame)




