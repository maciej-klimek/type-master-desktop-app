import customtkinter as ctk

class InputTextbox(ctk.CTkTextbox):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

    def create_input_textbox(self, frame):
        input_textbox = InputTextbox(
            frame,
            fg_color=("grey18"),
            width=600,
            height=60,
            font=("Cascadia Code", 16),
            border_color="grey30",
            border_width=2,
            wrap="word",
            
        )
        input_textbox.pack(expand=True, pady=50, padx=50)
        return input_textbox
