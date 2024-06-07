import customtkinter as ctk


class InputTextbox(ctk.CTkTextbox):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(
            self,
            fg_color=("grey18"),
            width=600,
            height=90,
            font=("Cascadia Code", 16),
            border_color="grey30",
            border_width=2,
            wrap="word",
        )
