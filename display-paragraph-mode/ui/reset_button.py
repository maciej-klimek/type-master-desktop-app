import customtkinter as ctk

class ResetButton():
    def __init__(self, parent):
        self.reset_button = ctk.CTkButton(
            parent,
            height=40,
            text="Reset",
            font=("Ubuntu", 16),
            fg_color="grey18",
            text_color="white",
            border_color="grey30",
            border_width=2,
            hover_color="grey30"
        )
        self.reset_button.pack(side="right", padx=[0, 50])
