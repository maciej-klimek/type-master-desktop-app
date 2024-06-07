import customtkinter as ctk


class HealthLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        HealthLabel.configure(
            self,
            text="[   ] [   ] [   ] [   ] [   ]",
            font=("Catamaran Bold", 20),
            corner_radius=8,
            justify="center",
            text_color="#844a4a"
        )
