import threading
from ui.ui_main import GUI
from ui.text_label import TextLabel
from ui.input_textbox import InputTextbox
from ui.speed_label import SpeedLabel
from ui.reset_button import ResetButton
import time
import random


class SentenceTest():
    def __init__(self):

        self.gui = GUI()
        self.running = False
        self.correct_chars_pressed = 0
        self.incorrect_chars_pressed = 0
        self.current_typing_index = 0

        self.get_new_text()

        self.gui.input_textbox.bind("<Button-1>", self.on_start)

        self.gui.reset_button.bind("<Button-1>", self.on_reset)
        self.gui.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.gui.run()

    def get_new_text(self, event=None):
        self.text_data = open("text_data.txt", "r").read().split("\n")
        self.correct_text = random.choice(self.text_data)
        self.hidden_correct_text = "".join(
            char if char == " " else "*" for char in self.correct_text
        )
        self.gui.text_label.configure(text=self.hidden_correct_text)

    def on_start(self, event=None):
        self.gui.input_textbox.bind("<Key>", self.on_key_press)
        self.gui.text_label.configure(text=self.correct_text)

    def on_key_press(self, event):
        # print("on_key_press")

        if event.keysym.lower() == "shift_l" or event.keysym.lower() == "shift_r":
            return

        typed_char = event.char

        if not self.running:
            self.running = True
            self.gui.input_textbox.delete("0.0", "end")
            self.writting_thread = threading.Thread(
                target=self.calculate_stats)
            self.writting_thread.daemon = True
            self.writting_thread.start()

        if typed_char == self.correct_text[self.current_typing_index]:
            # print("correct char pressed")
            self.gui.input_textbox.configure(text_color="#71c788")
            self.current_typing_index += 1
            self.correct_chars_pressed += 1

            if self.current_typing_index >= len(self.correct_text):
                self.running = False
                self.gui.input_textbox.unbind("<KeyPress>")
                self.gui.input_textbox.configure(state="disabled")
        else:
            # print("incorrect char pressed")
            self.incorrect_chars_pressed += 1
            self.gui.input_textbox.configure(text_color="#ab5555")
            return "break"

    def calculate_stats(self):
        counter = 0
        while self.running:
            time.sleep(0.05)
            counter += 0.1
            cps = self.current_typing_index / counter
            cpm = cps * 60
            if self.correct_chars_pressed != 0 and self.incorrect_chars_pressed != 0:
                accuracy = 100 * self.correct_chars_pressed / \
                    (self.correct_chars_pressed + self.incorrect_chars_pressed)
            else:
                accuracy = 0
            self.gui.speed_label.configure(
                text=f"Accuracy: {accuracy:.2f}%\nCPS: {cps:.2f}\nCPM: {cpm:.2f}")
        print("time_thread ended")

    def on_reset(self, event=None):
        self.get_new_text()
        self.running = False
        self.current_typing_index = 0
        self.correct_chars_pressed = 0
        self.incorrect_chars_pressed = 0
        self.gui.input_textbox.configure(state="normal")
        self.gui.input_textbox.delete("1.0", "end")
        print("reset")

    def on_closing(self):
        self.running = False
        self.gui.root.destroy()
        print("closing")


if __name__ == "__main__":
    SentenceTest()
