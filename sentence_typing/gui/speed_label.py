import customtkinter as ctk


class SpeedLabel(ctk.CTkButton):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        SpeedLabel.configure(
            self,
            text="WPM: 0\n CPM: 0\nCPS: 0",
            font=("Ubuntu", 16),
            text_color="grey30",
            fg_color="grey14",
            corner_radius=8,
            border_color="grey30",
            border_width=2,
            hover=False

        )
