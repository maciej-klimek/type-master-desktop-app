import customtkinter as ctk
from word_typing.gui.input_textbox import InputTextbox
from word_typing.gui.stat_label import StatLabel
from word_typing.gui.reset_button import ResetButton
from word_typing.gui.animation_box import AnimationBox
from word_typing.gui.level_label import LevelLabel
from word_typing.gui.title_label import TitleLabel
from config import BACKGROUND_COLOR

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("Dark")


class GUI(ctk.CTkFrame):
    def __init__(self, parent, word_typing_mode_instance):
        super().__init__(parent)
        self.root = parent
        self.word_typing_mode_instance = word_typing_mode_instance

        self.frame = ctk.CTkFrame(self.root, fg_color=BACKGROUND_COLOR)
        self.frame.pack(expand=True,  padx=20, pady=20)

        self.create_widgets()

    def run(self):
        self.root.mainloop()

    def create_widgets(self):

        top_frame = ctk.CTkFrame(self.frame, fg_color=BACKGROUND_COLOR)
        top_frame.pack(side="top")

        left_frame = ctk.CTkFrame(self.frame, fg_color=BACKGROUND_COLOR)
        left_frame.pack(side="left", padx=(0, 10))

        right_frame = ctk.CTkFrame(self.frame, fg_color=BACKGROUND_COLOR)
        right_frame.pack(side="right", padx=(10, 0))

        self.title_label = TitleLabel(top_frame)
        self.title_label.pack(expand=True, pady=[50, 50])

        self.animation_box = AnimationBox(
            left_frame, self.word_typing_mode_instance)

        self.input_textbox = InputTextbox(left_frame)
        self.input_textbox.pack(pady=(10, 50), padx=10)

        self.level_label = LevelLabel(right_frame)
        self.level_label.pack(pady=(10, 20), padx=10, ipadx=20, ipady=20)

        self.reset_button = ResetButton(right_frame)
        self.reset_button.pack(pady=(10, 10), padx=10)
