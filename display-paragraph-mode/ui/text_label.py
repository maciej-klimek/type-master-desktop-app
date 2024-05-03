import customtkinter as ctk

class TextLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

    def create_text_label(self, frame):
        label = TextLabel(
            frame,
            font=("Cascadia Code", 16),
            wraplength=600,
            justify='left',
            fg_color=("grey18"),
            corner_radius=8,
        )
        label.pack(fill="both", expand=True, ipady=50, ipadx=50)
        return label
