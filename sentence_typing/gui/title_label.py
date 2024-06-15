import customtkinter as ctk


class TitleLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(
            self,
            font=("Cascadia Code Bold", 35),
            justify='center',
        )
