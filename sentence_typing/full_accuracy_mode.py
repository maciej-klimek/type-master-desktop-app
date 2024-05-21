import threading
import logging
import sqlite3
import time
from sentence_typing.gui.gui_main import GUI
from config import SENTENCES_PATH, SPECIAL_KEYS

logging.basicConfig(level=logging.DEBUG)


class FullAccuracyMode():
    def __init__(self, parent):

        self.logger = logging.getLogger(__name__)
        self.gui = GUI(parent)

        self.running = False
        self.correct_chars_typed = 0
        self.incorrect_chars_typed = 0
        self.current_typing_index = 0

        try:
            self.get_new_text()
        except Exception as e:
            self.logger.error(f"Error initializing: {e}")

        self.gui.input_textbox.configure(state="disabled")
        self.gui.input_textbox.focus_set()

        self.gui.input_textbox.bind("<space>", self.on_start)
        self.gui.reset_button.bind("<Button-1>", self.on_reset)
        self.gui.run()

    def get_new_text(self, event=None):
        try:
            conn = sqlite3.connect(SENTENCES_PATH)
            cursor = conn.cursor()

            cursor.execute(
                'SELECT sentence FROM sentences ORDER BY RANDOM() LIMIT 1')
            result = cursor.fetchone()

            if result:
                self.correct_text = result[0]
                self.hidden_correct_text = "".join(
                    char if char == " " else "_" for char in self.correct_text
                )
                self.gui.text_label.configure(text=self.hidden_correct_text)

                # Print the sentence obtained from the database
                self.logger.debug(f"Sentence from database: {
                                  self.correct_text}")
            else:
                self.logger.error("No sentences found in the database.")

            conn.close()

        except sqlite3.Error as e:
            self.logger.error(f"Error reading text from database: {e}")

    def on_start(self, event=None):
        try:
            self.gui.input_textbox.configure(state="normal")
            self.gui.input_textbox.unbind("<space>")
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
            if self.gui.input_textbox.get(1.0) == " ":
                self.gui.input_textbox.delete(1.0)
            typed_char = event.char
            key_code = event.keysym

            if typed_char == self.correct_text[self.current_typing_index]:
                self.gui.input_textbox.configure(text_color="white")
                self.current_typing_index += 1
                self.correct_chars_typed += 1
                self.logger.debug("Correct char pressed: %s", typed_char)

                if self.current_typing_index >= len(self.correct_text):
                    self.running = False
                    self.gui.input_textbox.unbind("<KeyPress>")
                    self.gui.input_textbox.insert("end", ".")
                    self.gui.input_textbox.configure(state="disabled")
            elif key_code not in SPECIAL_KEYS:
                self.incorrect_chars_typed += 1
                self.gui.input_textbox.configure(
                    text_color=self.gui.GRADE_COLOR_PALLETE["worst"])
                self.logger.debug("Incorrect char pressed: %s", typed_char)
                return "break"
        except Exception as e:
            self.logger.error(f"Error processing key press: {e}")

    def calculate_stats(self):
        try:
            start_time = time.time()
            while self.running:
                time_elapsed = time.time() - start_time
                if time_elapsed > 0:
                    wpm = 60 * len(self.gui.input_textbox.get(
                        0.0, "end").split()) / time_elapsed
                    cps = self.current_typing_index / time_elapsed
                    cpm = cps * 60
                    if self.correct_chars_typed != 0:
                        accuracy = 100 * self.correct_chars_typed / \
                            (self.correct_chars_typed + self.incorrect_chars_typed)
                    else:
                        accuracy = 0
                    self.gui.speed_label.configure(
                        text=f"WPM: {wpm:.2f}\nCPM: {cpm: .2f}\nCPS: {cps: .2f}")
                    self.gui.accuracy_label.configure(
                        text=f"Accuracy: {accuracy: .2f}%")
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

                    if accuracy > 95:
                        self.gui.accuracy_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["great"])
                    elif accuracy > 90:
                        self.gui.accuracy_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["good"])
                    elif accuracy > 80:
                        self.gui.accuracy_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["average"])
                    elif accuracy > 70:
                        self.gui.accuracy_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["bad"])
                    else:
                        self.gui.accuracy_label.configure(
                            text_color=self.gui.GRADE_COLOR_PALLETE["worst"])

                # time.sleep(0.05)  # Adjust this value as needed for performance
        except Exception as e:
            self.logger.error(f"Error calculating stats: {e}")

    def on_reset(self, event=None):
        try:
            self.get_new_text()
            self.gui.input_textbox.configure(state="normal")
            self.current_typing_index = 0
            self.correct_chars_typed = 0
            self.incorrect_chars_typed = 0
            self.gui.input_textbox.unbind("<Key>")
            self.gui.input_textbox.delete("1.0", "end")
            self.gui.input_textbox.bind("<space>", self.on_start)
            self.gui.input_textbox.configure(text_color="white")
            self.gui.input_textbox.configure(state="disabled")

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
    FullAccuracyMode()
