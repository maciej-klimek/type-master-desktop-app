import customtkinter as ctk
from sentence_typing.full_accuracy_mode import FullAccuracyMode
from sentence_typing.measure_accuracy_mode import MeasureAccuracyMode
from word_typing.word_typing_mode import WordTypingMode
from config import BACKGROUND_COLOR, SELECTION_COLOR, FAC_COLOR, MAC_COLOR, WTG_COLOR
from db.database_manager import DatabaseManager
from PIL import Image

ctk.set_appearance_mode("Dark")


class ModeButton(ctk.CTkButton):
    def __init__(self, master=None, **kwargs):
        self.command = kwargs.pop("command", None)
        super().__init__(master, **kwargs)
        self.active = False
        self.configure(
            height=40,
            font=("Ubuntu", 14),
            fg_color="grey18",
            border_color="grey30",
            border_width=2,
            hover_color=SELECTION_COLOR,
            command=self.toggle_active
        )

    def toggle_active(self):
        self.active = True
        self.update_colors()
        if self.command:
            self.command()

    def update_colors(self):
        for child in self.master.winfo_children():
            if isinstance(child, ModeButton) and child != self:
                child.active = False
                child.configure(fg_color="grey18")
        self.configure(fg_color=SELECTION_COLOR)


class MainMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.root = parent
        self.root.title("TypeMaster")
        self.root.geometry("1400x900")
        self.configure(fg_color=BACKGROUND_COLOR)
        self.settings_image = ctk.CTkImage(Image.open("settings_icon.png"))

        self.create_widgets()

    def run(self):
        self.pack(fill="y", expand="y")
        self.root.attributes('-fullscreen', False)
        self.is_fullscreen_open = False
        self.root.bind("<F11>", self.change_fullscreen)
        self.root.mainloop()

    def create_widgets(self):
        self.mode_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        self.mode_frame.pack(expand=True, fill="both")

        mode_buttons_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        mode_buttons_frame.place(relx=0.51, rely=1.0, anchor="s", y=-30)
        self.show_title_screen()

        self.btn_full_accuracy = ModeButton(
            mode_buttons_frame, text="Full Typing Accuracy Mode", command=self.open_full_accuracy_mode, text_color=FAC_COLOR)
        self.btn_full_accuracy.pack(side="left", padx=10)

        self.btn_measure_accuracy = ModeButton(
            mode_buttons_frame, text="Measure Typing Accuracy Mode", command=self.open_measure_accuracy_mode, text_color=MAC_COLOR)
        self.btn_measure_accuracy.pack(side="left", padx=10)

        self.btn_word_typing = ModeButton(
            mode_buttons_frame, text="Word Typing Mode", command=self.open_word_game_mode, text_color=WTG_COLOR)
        self.btn_word_typing.pack(side="left", padx=10)

        self.btn_database_manager = ctk.CTkButton(
            mode_buttons_frame,
            text="",
            width=40,
            height=40,
            fg_color=BACKGROUND_COLOR,
            hover_color=SELECTION_COLOR,
            image=self.settings_image,
            command=self.open_database_manager)
        self.btn_database_manager.pack(side="left", padx=10)

    def show_title_screen(self):
        self.destroy_mode_frame_content()
        title_label = ctk.CTkLabel(
            self.mode_frame, text="Title Screen", font=("Arial", 60), width=1000, height=600)
        title_label.pack(expand=True)

    def open_full_accuracy_mode(self):
        self.update_button_states(self.btn_full_accuracy)
        self.destroy_mode_frame_content()
        FullAccuracyMode(self.mode_frame)

    def open_measure_accuracy_mode(self):
        self.update_button_states(self.btn_measure_accuracy)
        self.destroy_mode_frame_content()
        MeasureAccuracyMode(self.mode_frame)

    def open_word_game_mode(self):
        self.update_button_states(self.btn_word_typing)
        self.destroy_mode_frame_content()
        WordTypingMode(self.mode_frame)

    def open_database_manager(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")
        app = DatabaseManager()
        app.mainloop()

    def update_button_states(self, active_button):
        self.btn_full_accuracy.configure(fg_color="grey18")
        self.btn_measure_accuracy.configure(fg_color="grey18")
        self.btn_word_typing.configure(fg_color="grey18")

        active_button.configure(fg_color=SELECTION_COLOR)

    def destroy_mode_frame_content(self):
        for widget in self.mode_frame.winfo_children():
            widget.destroy()

    def change_fullscreen(self, event=None):
        if self.is_fullscreen_open == False:
            self.root.attributes('-fullscreen', True)
            self.is_fullscreen_open = True
        else:
            self.root.attributes('-fullscreen', False)
            self.is_fullscreen_open = False


if __name__ == "__main__":
    root = ctk.CTk()
    MainMenu(root).run()
