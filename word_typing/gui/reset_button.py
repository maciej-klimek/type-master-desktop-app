import customtkinter as ctk


class ResetButton(ctk.CTkButton):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(
            self,
            height=40,
            text="Reset",
            font=("Ubuntu", 16),
            fg_color="grey18",
            text_color="white",
            border_color="grey30",
            border_width=2,
            hover_color="grey30"
        )
        self.pack(expand=True)
