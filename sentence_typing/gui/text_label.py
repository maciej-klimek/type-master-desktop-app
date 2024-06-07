import customtkinter as ctk


class TextLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(
            self,
            font=("Cascadia Code", 16),
            wraplength=600,
            justify='left',
            fg_color=("grey18"),
            corner_radius=8,
        )
