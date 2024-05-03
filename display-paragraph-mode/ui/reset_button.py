import customtkinter as ctk

class ResetButton(ctk.CTkButton):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

    def create_reset_button(self, frame):
        reset_button = ResetButton(
            frame,
            height=40,
            text="Reset",
            font=("Ubuntu", 16),
            fg_color="grey18",
            text_color="white",
            border_color="grey30",
            border_width=2,
            hover_color="grey30"
        )
        reset_button.pack(side="right", padx=[0, 50])
        return reset_button
