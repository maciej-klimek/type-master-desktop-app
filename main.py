import customtkinter as ctk
from sentence_typing.full_accuracy_mode import FullAccuracyMode
from sentence_typing.measure_accuracy_mode import MeasureAccuracyMode
from word_typing.word_typing_mode import LeftToRightMode

ctk.set_appearance_mode("Dark")


class MainMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.root = parent
        self.root.title("TypeMaster")
        self.root.geometry("1000x800")
        self.configure(fg_color="grey14")

        self.create_widgets()

    def run(self):
        self.pack(expand=True)
        self.root.mainloop()

    def create_widgets(self):
        self.mode_frame = ctk.CTkFrame(self, fg_color="grey14")
        self.mode_frame.pack(expand=True, fill="both")

        self.show_title_screen()

        buttons_frame = ctk.CTkFrame(self, fg_color="grey14")
        buttons_frame.pack(side="bottom", pady=10)

        btn_full_accuracy = ctk.CTkButton(
            buttons_frame, text="Full Typing Accuracy Mode", command=self.open_full_accuracy_mode)
        btn_full_accuracy.configure(
            height=40,
            font=("Ubuntu", 16),
            fg_color="grey18",
            text_color="white",
            border_color="grey30",
            border_width=2,
            hover_color="grey30"
        )
        btn_full_accuracy.pack(side="left", padx=10)

        btn_measure_accuracy = ctk.CTkButton(
            buttons_frame, text="Measure Typing Accuracy Mode", command=self.open_measure_accuracy_mode)
        btn_measure_accuracy.configure(
            height=40,
            font=("Ubuntu", 16),
            fg_color="grey18",
            text_color="white",
            border_color="grey30",
            border_width=2,
            hover_color="grey30"
        )
        btn_measure_accuracy.pack(side="left", padx=10)

        btn_for_left_to_right_mode = ctk.CTkButton(
            buttons_frame, text="Word Typing Mode", command=self.open_word_game_mode)
        btn_for_left_to_right_mode.configure(
            height=40,
            font=("Ubuntu", 16),
            fg_color="grey18",
            text_color="white",
            border_color="grey30",
            border_width=2,
            hover_color="grey30"
        )
        btn_for_left_to_right_mode.pack(side="left", padx=10)

    def show_title_screen(self):
        self.destroy_mode_frame_content()
        title_label = ctk.CTkLabel(
            self.mode_frame, text="Title Screen", font=("Arial", 24))
        title_label.pack(expand=True)

    def open_full_accuracy_mode(self):
        self.destroy_mode_frame_content()
        FullAccuracyMode(self.mode_frame)

    def open_measure_accuracy_mode(self):
        self.destroy_mode_frame_content()
        MeasureAccuracyMode(self.mode_frame)

    def open_word_game_mode(self):
        self.destroy_mode_frame_content()
        LeftToRightMode(self.mode_frame)

    def destroy_mode_frame_content(self):
        for widget in self.mode_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    MainMenu(root).run()
