import customtkinter as ctk


class LevelLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        LevelLabel.configure(
            self,
            width=150,
            text="Naciśnij enter\nżeby rozpocząć\ngrę!",
            font=("Cascadia Code Bold", 16),
            corner_radius=8,
            justify="left",
            fg_color="#71c788",
            text_color="black",
        )
