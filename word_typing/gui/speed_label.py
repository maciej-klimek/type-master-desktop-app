import customtkinter as ctk


class SpeedLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        SpeedLabel.configure(
            self,
            text="Level: 1 \nCorrect words: 0\nNext level: 0",
            font=("Ubuntu", 16),
            corner_radius=8,
            justify="left",
            fg_color="#71c788",
            text_color="black",
        )
#pushujemy widzowie