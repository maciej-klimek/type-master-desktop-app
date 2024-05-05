import threading
import logging
import random
import time
from gui.gui_main import GUI

logging.basicConfig(level=logging.DEBUG)

SPECIAL_KEYS = {
    "Shift_L": "Left Shift",
    "Shift_R": "Right Shift",
    "Control_L": "Left Ctrl",
    "Control_R": "Right Ctrl",
    "Alt_L": "Left Alt",
    "Alt_R": "Right Alt",
    "Caps_Lock": "Caps Lock"
}


class FullAccuracyMode():
    def __init__(self):

        self.logger = logging.getLogger(__name__)
        self.gui = GUI()

        self.running = False
        self.correct_chars_typed = 0
        self.incorrect_chars_typed = 0
        self.current_typing_index = 0

        try:
            self.get_new_text()
        except Exception as e:
            self.logger.error(f"Error initializing: {e}")

        self.gui.input_textbox.bind("<Button-1>", self.on_start)
        self.gui.reset_button.bind("<Button-1>", self.on_reset)
        self.gui.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.gui.run()

    def get_new_text(self, event=None):
        try:
            self.text_data = open("text_data.txt", "r").read().split("\n")
            self.correct_text = random.choice(self.text_data)
            self.hidden_correct_text = "".join(
                char if char == " " else "*" for char in self.correct_text
            )
            self.gui.text_label.configure(text=self.hidden_correct_text)
        except FileNotFoundError as e:
            self.logger.error(f"Error reading text file: {e}")

    def on_start(self, event=None):
        try:
            self.gui.input_textbox.bind("<Key>", self.on_key_press)
            self.gui.text_label.configure(text=self.correct_text)
            self.logger.info("START")
            if not self.running:
                self.running = True
                self.writting_thread = threading.Thread(
                    target=self.calculate_stats)
                self.writting_thread.daemon = True
                self.writting_thread.start()
        except Exception as e:
            self.logger.error(f"Error starting thread: {e}")

    def on_key_press(self, event):
        try:
            typed_char = event.char
            key_code = event.keysym

            if typed_char == self.correct_text[self.current_typing_index]:
                self.gui.input_textbox.configure(text_color="#71c788")
                self.current_typing_index += 1
                self.correct_chars_typed += 1
                self.logger.debug("Correct char pressed: %s", typed_char)

                if self.current_typing_index >= len(self.correct_text):
                    self.running = False
                    self.gui.input_textbox.unbind("<KeyPress>")
                    self.gui.input_textbox.configure(state="disabled")
            elif key_code not in SPECIAL_KEYS:
                self.incorrect_chars_typed += 1
                self.gui.input_textbox.configure(text_color="#ab5555")
                self.logger.debug("Incorrect char pressed: %s", typed_char)
                return "break"
        except Exception as e:
            self.logger.error(f"Error processing key press: {e}")

    def calculate_stats(self):
        try:
            counter = 0
            while self.running:
                time.sleep(0.05)
                counter += 0.1
                cps = self.current_typing_index / counter
                cpm = cps * 60
                if self.correct_chars_typed != 0:
                    accuracy = 100 * self.correct_chars_typed / \
                        (self.correct_chars_typed + self.incorrect_chars_typed)
                else:
                    accuracy = 0
                self.gui.speed_label.configure(
                    text=f"Accuracy: {accuracy:.2f}%\nCPS: {cps:.2f}\nCPM: {cpm:.2f}")
        except Exception as e:
            self.logger.error(f"Error calculating stats: {e}")

    def on_reset(self, event=None):
        try:
            self.get_new_text()
            self.current_typing_index = 0
            self.correct_chars_typed = 0
            self.incorrect_chars_typed = 0
            self.gui.input_textbox.unbind("<Key>")
            self.gui.input_textbox.delete("0.0", "end")
            self.gui.input_textbox.configure(text_color="white")
            self.logger.info("RESET")
        except Exception as e:
            self.logger.error(f"Error resetting GUI: {e}")

    def on_closing(self):
        try:
            self.running = False
            self.gui.root.destroy()
            self.logger.info("CLOSE")
        except Exception as e:
            self.logger.error(f"Error closing application: {e}")


if __name__ == "__main__":
    FullAccuracyMode()
