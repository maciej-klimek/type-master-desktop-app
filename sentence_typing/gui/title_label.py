import customtkinter as ctk


class TitleLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(
            self,
            font=("Ubuntu", 30),
            justify='center',
        )
        self.pack(fill="both", expand=True, pady=[0, 50])
