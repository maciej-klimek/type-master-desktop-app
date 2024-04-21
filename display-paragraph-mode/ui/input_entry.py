import customtkinter as ctk

class InputLabel():
    def __init__(self, parent):
        input_textbox = ctk.CTkTextbox(
            self.frame,
            fg_color=("grey18"),
            width=600,
            height=60,
            font=("Cascadia Code", 16),
            border_color="grey30",
            border_width=2,
            wrap="word"
        )
        self.input_textbox.pack(expand=True, pady=50, padx=50)
