import customtkinter as ctk


class SpeedLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        SpeedLabel.configure(
            self,
            text="WPM: 0\n CPM: 0\nCPS: 0",
            font=("Ubuntu", 16),
            corner_radius=8,
            justify="left",
            fg_color="#71c788",
            text_color="black",
        )
        self.pack(side="left", ipadx=20, ipady=20)
