import customtkinter as ctk


class TimeLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        TimeLabel.configure(
            self,
            text="Time elapsed: 0 seconds",
            font=("Ubuntu", 16),
            corner_radius=8,
            justify="right",
            text_color="grey30",
        )
