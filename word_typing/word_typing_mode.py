import random
import time
import logging
import threading
from word_typing.gui.gui_main import GUI
from config import WORDS_PATH

logging.basicConfig(level=logging.DEBUG)


class WordTypingMode():
    def __init__(self, parent):

        self.logger = logging.getLogger(__name__)
        self.gui = GUI(parent)

        self.running = False
        self.correct_words_typed = 0
        self.incorrect_words_typed = 0
        self.current_typing_index = 0

        self.gui.input_textbox.bind("<KeyRelease>", self.on_key_press)
        self.gui.reset_button.bind("<Button-1>", self.on_reset)

        self.gui.run()

    def on_start(self, event=None):
        self.logger.debug("START")

    def on_key_press(self, event):
        input_word = self.gui.input_textbox.get("1.0", "end-1c").strip()
        if input_word in self.gui.words_label.generated_words:
            self.gui.words_label.generated_words.remove(input_word)
            self.gui.input_textbox.delete("1.0", "end")
            self.correct_words_typed += 1
            self.gui.words_label.remove_word_from_canvas(input_word)

    def calculate_stats(self):
        try:
            start_time = time.time()
            while self.running:
                time_elapsed = time.time() - start_time
                if time_elapsed > 0:
                    wpm = 60 * (self.correct_words_typed / time_elapsed)
        except Exception as e:
            self.logger.error(f"Error resetting GUI: {e}")


    def on_reset(self, event=None):
        try:
            self.correct_words_typed = 0
            self.incorrect_words_typed = 0
            self.gui.input_textbox.unbind("<KeyRelease>")
            self.gui.input_textbox.delete("1.0", "end")
            self.gui.words_label.reset_words()
            self.gui.input_textbox.bind("<KeyRelease>", self.on_key_press)
            self.logger.debug("RESET")
        except Exception as e:
            self.logger.error(f"Error resetting GUI: {e}")

    def on_closing(self):
        try:
            self.running = False
            self.gui.root.destroy()
            self.logger.debug("CLOSE")
        except Exception as e:
            self.logger.error(f"Error closing: {e}")


if __name__ == "__main__":
    WordTypingMode()