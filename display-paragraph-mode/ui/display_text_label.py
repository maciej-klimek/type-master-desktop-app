import random
from tkinter import ttk


class display_text_label():
    def __init__(self):
        text = random.choice(self.text_data)
        label = ttk.CTkLabel(
            self.frame,
            text=text,
            font=("Cascadia Code", 16),
            wraplength=600,
            height=200,
            justify='left',
            fg_color=("grey18"),
            corner_radius=8
        )
        label.grid(row=0, column=0, columnspan=2,
                   padx=100, pady=[100, 0], ipady=50, ipadx=50)
        self.text_label = text
