import customtkinter as ctk

class SpeedLabel():
    def __init__(self, parent):
        speed_label = ctk.CTkLabel(
            self.frame,
            text="Accuracy: 0% \nCPS: 0\nCPM: 0",
            font=("Ubuntu", 16),
            corner_radius=8,
            justify="left",
            fg_color="#71c788",
            text_color="black",

        )
        self.speed_label.pack(side="left", padx=[50, 0], ipadx=20, ipady=20)
