import customtkinter as ctk
from word_typing.gui.input_textbox import InputTextbox
from word_typing.gui.reset_button import ResetButton
from word_typing.gui.word_animation_box import WordAnimationBox
from word_typing.gui.speed_label import SpeedLabel

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("Dark")


class GUI(ctk.CTkFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.root = parent

        self.frame = ctk.CTkFrame(self.root, fg_color="grey14")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.create_widgets()

    def run(self):
        self.root.mainloop()

    def create_widgets(self):
        left_frame = ctk.CTkFrame(self.frame, fg_color="grey14")
        left_frame.pack(side="left", padx=(0, 10))

        right_frame = ctk.CTkFrame(self.frame, fg_color="grey14")
        right_frame.pack(side="right", padx=(10, 0))

        self.words_label = WordAnimationBox(left_frame)
        self.words_label.pack(expand=True, fill="both", pady=(0, 10))

        self.input_textbox = InputTextbox(left_frame)
        self.input_textbox.pack(pady=(10, 20), padx=10, fill="x")

        self.reset_button = ResetButton(right_frame)
        self.reset_button.pack(pady=(10, 10), padx=10)

        self.speed_label = SpeedLabel(right_frame)
        self.speed_label.pack(pady=(10, 20), padx=10)
