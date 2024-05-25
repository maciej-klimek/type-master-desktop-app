import customtkinter as ctk
from config import WTG_COLOR


class TitleLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(
            self,
            font=("Ubuntu", 30),
            justify='center',
            text="Word Typing Game Mode",
            text_color=WTG_COLOR
        )
