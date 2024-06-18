from .reset_button import ResetButton
from .speed_label import SpeedLabel
from .accuracy_label import AccuracyLabel
from .time_label import TimeLabel
from .input_textbox import InputTextbox
from .text_label import TextLabel
from .title_label import TitleLabel
import customtkinter as ctk

ctk.set_appearance_mode("Dark")


class GUI(ctk.CTkFrame):
    def __init__(self, parent, title, title_color):
        self.root = parent

        self.title = title
        self.title_color = title_color

        self.main_frame = ctk.CTkFrame(self.root, fg_color="grey14")
        self.stats_frame = ctk.CTkFrame(self.main_frame, fg_color="grey14")

        self.GRADE_COLOR_PALLETE = {
            "great":  "#85cf5b",
            "good":  "#91c771",
            "average":  "#d6ce56",
            "bad":  "#cc915a",
            "worst":  "#cc6f5a",
        }

        self.create_widgets()

    def run(self):
        self.main_frame.pack(expand=True, padx=200)
        self.stats_frame.pack(fill="x", side="left", padx=[50, 0])
        self.root.mainloop()

    def create_widgets(self):
        self.title_label = TitleLabel(
            self.main_frame, text=self.title, text_color=self.title_color)
        self.title_label.pack(fill="both", expand=True, pady=[0, 50])

        self.text_label = TextLabel(self.main_frame)
        self.text_label.pack(fill="both", expand=True, ipady=50, ipadx=50)

        self.time_label = TimeLabel(self.main_frame)
        self.time_label.pack()

        self.input_textbox = InputTextbox(self.main_frame)
        self.input_textbox.pack(expand=True, pady=[50, 0], padx=50)

        self.accuracy_label = AccuracyLabel(self.stats_frame)
        self.accuracy_label.pack(pady=[5, 30])

        self.speed_label = SpeedLabel(self.stats_frame)
        self.speed_label.pack(side="left", ipadx=5, ipady=20)

        self.reset_button = ResetButton(self.main_frame)
        self.reset_button.pack(side="right", padx=[0, 50], pady=[50, 0])
