from .reset_button import ResetButton
from .speed_label import SpeedLabel
from .accuracy_label import AccuracyLabel
from .time_label import TimeLabel
from .input_textbox import InputTextbox
from .text_label import TextLabel
import customtkinter as ctk

ctk.set_appearance_mode("Dark")


class GUI(ctk.CTkFrame):
    def __init__(self, parent):
        self.root = parent  # Set the root window to the parent component

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
        self.main_frame.pack(expand=True)
        self.stats_frame.pack(fill="x", side="left", padx=[50, 0])
        self.root.mainloop()

    def create_widgets(self):
        self.text_label = TextLabel(self.main_frame)
        self.time_label = TimeLabel(self.main_frame)

        self.input_textbox = InputTextbox(self.main_frame)
        self.accuracy_label = AccuracyLabel(self.stats_frame)

        self.speed_label = SpeedLabel(self.stats_frame)
        self.reset_button = ResetButton(self.main_frame)
