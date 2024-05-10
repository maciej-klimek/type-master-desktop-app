import threading
import logging
import random
import time
from gui.gui_main import GUI

logging.basicConfig(level=logging.INFO)

SPECIAL_KEYS = {
    "Shift_L": "Left Shift",
    "Shift_R": "Right Shift",
    "Control_L": "Left Ctrl",
    "Control_R": "Right Ctrl",
    "Alt_L": "Left Alt",
    "Alt_R": "Right Alt",
    "Caps_Lock": "Caps Lock"
}


class MeasureAccuracyMode():
    def __init__(self):

        self.logger = logging.getLogger(__name__)
        self.gui = GUI()

        self.running = False
        self.chars_typed = 0
        self.accuracy = 0

        try:
            self.load_text_thread = threading.Thread(target=self.get_new_text)
            self.load_text_thread.daemon = True
            self.load_text_thread.start()
        except Exception as e:
            self.logger.error(f"Error initializing: {e}")

        self.gui.input_textbox.bind("<Button-1>", self.on_start)
        self.gui.reset_button.bind("<Button-1>", self.on_reset)
        self.gui.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.gui.run()

    def get_new_text(self):
        try:
            self.text_data = open("text_data.txt", "r").read().split("\n")
            self.correct_text = random.choice(self.text_data)
            self.correct_text_words = self.correct_text.split()
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
                self.calculate_stats_thread = threading.Thread(
                    target=self.calculate_stats)
                self.calculate_stats_thread.daemon = True
                self.calculate_stats_thread.start()
        except Exception as e:
            self.logger.error(f"Error starting thread: {e}")

    def on_key_press(self, event):
        try:
            key_code = event.keysym
            if key_code == "Return":
                self.running = False
                self.gui.input_textbox.unbind("<KeyPress>")
                self.logger.debug("enter pressed")
            elif key_code == "BackSpace":
                self.logger.debug("backspace pressed")
                if self.chars_typed > 0:
                    self.chars_typed -= 1
                    self.logger.debug("backspace pressed and deleted a char")

            elif key_code not in SPECIAL_KEYS:
                self.chars_typed += 1

            self.logger.debug(self.chars_typed)

            self.calculate_accuracy(self.gui.input_textbox.get(0.0, "end"))
        except Exception as e:
            self.logger.error(f"Error processing key press: {e}")

    def calculate_stats(self):
        try:
            start_time = time.time()
            while self.running:
                time_elapsed = time.time() - start_time
                if time_elapsed > 0:  # Avoid division by zero
                    wpm = 60 * len(self.gui.input_textbox.get(
                        0.0, "end").split()) / time_elapsed
                    cps = self.chars_typed / time_elapsed
                    cpm = cps * 60
                    self.gui.speed_label.configure(
                        text=f"WPM: {wpm:.2f}\nCPM: {cpm:.2f}\nCPS: {cps:.2f}")
                    self.gui.accuracy_label.configure(
                        text=f"Accuracy: {self.accuracy:.2f}%")
                    self.gui.time_label.configure(
                        text=f"Time elapsed: {time_elapsed: .1f} seconds.")

                    if wpm > 50:
                        self.gui.speed_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["great"])
                    elif wpm > 45:
                        self.gui.speed_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["good"])
                    elif wpm > 40:
                        self.gui.speed_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["average"])
                    elif wpm > 35:
                        self.gui.speed_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["bad"])
                    else:
                        self.gui.speed_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["worst"])

                    if self.accuracy > 95:
                        self.gui.accuracy_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["great"])
                    elif self.accuracy > 90:
                        self.gui.accuracy_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["good"])
                    elif self.accuracy > 80:
                        self.gui.accuracy_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["average"])
                    elif self.accuracy > 70:
                        self.gui.accuracy_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["bad"])
                    else:
                        self.gui.accuracy_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["worst"])
        except Exception as e:
            self.logger.error(f"Error calculating stats: {e}")

    def calculate_accuracy(self, user_input):
        try:
            correct_chars_typed = 0
            incorrect_chars_typed = 0
            user_input_words = user_input.split()
            correct_text_words = self.correct_text_words[0:len(
                user_input_words)]
            self.logger.debug(f"User input: {user_input_words}   |   Correct text: {
                              correct_text_words}")

            for user_word, correct_word in zip(user_input_words, correct_text_words):
                try:
                    for i, letter in enumerate(user_word):
                        if letter == correct_word[i]:
                            correct_chars_typed += 1
                        else:
                            incorrect_chars_typed += 1
                except IndexError:
                    incorrect_chars_typed += abs(len(user_word) - i)

            if correct_chars_typed:
                self.accuracy = 100 * correct_chars_typed / \
                    (correct_chars_typed + incorrect_chars_typed)
            else:
                self.accuracy = 0
            self.logger.debug(f"Accuracy: {self.accuracy} %")
        except Exception as e:
            self.logger.error(f"Error calculating accuracy: {e}")

    def on_reset(self, event=None):
        try:
            self.get_new_text()
            self.chars_typed = 0
            self.gui.input_textbox.unbind("<Key>")
            self.gui.input_textbox.delete("0.0", "end")
            self.gui.input_textbox.configure(text_color="white")
            self.running = False
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
    MeasureAccuracyMode()
