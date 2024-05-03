import threading
import logging
import random
import time
from gui.gui_main import GUI

logging.basicConfig(level=logging.DEBUG)


class FullAccuracyMode():
    def __init__(self):

        self.logger = logging.getLogger(__name__)
        self.gui = GUI()

        self.running = False
        self.correct_chars_typed = 0
        self.incorrect_chars_typed = 0
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
        self.logger.debug("start")

    def on_key_press(self, event):
        typed_char = event.char

        if not self.running:
            self.running = True
            self.writting_thread = threading.Thread(
                target=self.calculate_stats)
            self.writting_thread.daemon = True
            self.writting_thread.start()

        # DEBUG
        # self.logger.debug("Correct text: %s\nTyped text: %s",
        #                   self.correct_text, self.gui.input_textbox.get("0.0", "end"))

        # self.logger.debug("Expected char: %s",
        #                   self.correct_text[self.current_typing_index])

        if typed_char == self.correct_text[self.current_typing_index]:
            # self.logger.debug("Correct char pressed: %s", typed_char)
            self.gui.input_textbox.configure(text_color="#71c788")
            self.current_typing_index += 1
            self.correct_chars_typed += 1

            if self.current_typing_index >= len(self.correct_text):
                self.running = False
                self.gui.input_textbox.unbind("<KeyPress>")
                self.gui.input_textbox.configure(state="disabled")
        else:
            # self.logger.debug("Incorrect char pressed: %s", typed_char)
            self.incorrect_chars_typed += 1
            self.gui.input_textbox.configure(text_color="#ab5555")
            return "break"

    def calculate_stats(self):
        counter = 0
        while self.running:
            time.sleep(0.05)
            counter += 0.1
            cps = self.current_typing_index / counter
            cpm = cps * 60
            if self.correct_chars_typed != 0 and self.incorrect_chars_typed != 0:
                accuracy = 100 * self.correct_chars_typed / \
                    (self.correct_chars_typed + self.incorrect_chars_typed)
            else:
                accuracy = 0
            self.gui.speed_label.configure(
                text=f"Accuracy: {accuracy:.2f}%\nCPS: {cps:.2f}\nCPM: {cpm:.2f}")

    def on_reset(self, event=None):
        self.get_new_text()
        self.current_typing_index = 0
        self.correct_chars_typed = 0
        self.incorrect_chars_typed = 0
        self.gui.input_textbox.unbind("<Key>")
        self.gui.input_textbox.delete("0.0", "end")
        self.gui.input_textbox.configure(text_color="white")
        self.logger.debug("reset")

    def on_closing(self):
        self.running = False
        self.gui.root.destroy()
        self.logger.debug("closing")


if __name__ == "__main__":
    FullAccuracyMode()
