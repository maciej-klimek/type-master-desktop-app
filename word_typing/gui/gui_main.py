import customtkinter as ctk
from word_typing.gui.input_textbox import InputTextbox
from word_typing.gui.stat_label import StatLabel
from word_typing.gui.reset_button import ResetButton
from word_typing.gui.animation_box import AnimationBox
from word_typing.gui.level_label import LevelLabel
from word_typing.gui.title_label import TitleLabel
from word_typing.gui.health_label import HealthLabel
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
        top_frame.pack(side="top", fill="x")

        bottom_frame = ctk.CTkFrame(self.frame, fg_color=BACKGROUND_COLOR)
        bottom_frame.pack(side="top", fill="x")

        # Configure grid weights to ensure proper spacing
        bottom_frame.grid_columnconfigure(0, weight=0)  # left space
        bottom_frame.grid_columnconfigure(1, weight=1)  # center frame
        # right space (level_label and reset_button)
        bottom_frame.grid_columnconfigure(2, weight=0)

        self.title_label = TitleLabel(top_frame)
        self.title_label.pack(pady=[0, 50])

        self.animation_box = AnimationBox(
            top_frame, self.word_typing_mode_instance)

        self.reset_button = ResetButton(bottom_frame)
        self.reset_button.grid(row=1, column=0)

        self.health_label = HealthLabel(bottom_frame)
        self.health_label.grid(row=0, column=1, pady=[10, 0])

        self.input_textbox = InputTextbox(bottom_frame)
        self.input_textbox.grid(row=1, column=1)

        self.level_label = LevelLabel(bottom_frame)
        self.level_label.grid(row=1, column=2, ipadx=10, ipady=10, sticky="n")
