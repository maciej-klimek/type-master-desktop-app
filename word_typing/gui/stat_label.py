import customtkinter as ctk


class StatLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        StatLabel.configure(
            self,
            text="wpm: 0 \nCorrect words: 0\nIncorrect words: 0",
            font=("Ubuntu", 16),
            corner_radius=8,
            justify="left",
            fg_color="#71c788",
            text_color="black",
        )