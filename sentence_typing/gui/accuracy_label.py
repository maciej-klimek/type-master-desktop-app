import customtkinter as ctk


class AccuracyLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        AccuracyLabel.configure(
            self,
            text="Naciśnij spacje żeby rozpocząć!",
            font=("Cascadia Code Bold", 16),
            corner_radius=8,
            justify="left",
            text_color="grey30",
        )
