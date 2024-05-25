import random
import time
import logging
import threading
from word_typing.gui.gui_main import GUI
from config import WORDS_PATH
from word_typing.gui.word_animation_box import WordAnimationBox

logging.basicConfig(level=logging.DEBUG)


class WordTypingMode:
    def __init__(self, parent):
        self.logger = logging.getLogger(__name__)
        self.gui = GUI(parent, self)  # Pass self to GUI

        self.running = False
        self.correct_words_typed = 0
        self.incorrect_words_typed = 0
        self.current_typing_index = 0
        self.game_reset = False  # Flag to check if the game is in a reset state

        self.gui.input_textbox.bind("<KeyRelease>", self.on_key_press)
        self.gui.reset_button.bind("<Button-1>", self.on_reset)
        self.gui.input_textbox.bind("<Return>", self.on_start)

        self.gui.run()

    def on_start(self, event=None):
        if self.running:
            return

        if self.game_reset:  # Check if the game is in a reset state
            self.logger.debug("START AFTER RESET")
            self.running = True
            self.gui.word_animation_box.start_game()
            self.game_reset = False  # Reset the flag
        else:
            self.logger.debug("START")
            self.running = True
            self.gui.word_animation_box.start_game()

    def on_key_press(self, event):
        input_word = self.gui.input_textbox.get("1.0", "end-1c").strip()
        self.logger.debug(input_word)
        if input_word in self.gui.word_animation_box.generated_words:
            self.gui.word_animation_box.generated_words.remove(input_word)
            self.gui.input_textbox.delete("1.0", "end")
            self.correct_words_typed += 1
            self.gui.word_animation_box.remove_word_from_canvas(input_word)

    def calculate_stats(self):
        try:
            start_time = time.time()
            while self.running:
                time_elapsed = time.time() - start_time
                if time_elapsed > 0:
                    wpm = 60 * self.correct_words_typed / time_elapsed
                    self.gui.speed_label.configure(text=f"WPM: {wpm:.2f}")

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
                time.sleep(0.1)
        except Exception as e:
            self.logger.error(f"Error calculating stats: {e}")

    def on_reset(self, event=None):
        self.gui.input_textbox.bind("<Return>", self.on_start)
        self.gui.input_textbox.unbind("<KeyRelease>")
        self._reset_game_state()
        self.logger.debug("RESET")

    def reset_game_due_to_fallen_words(self):
        self._reset_game_state()
        self.logger.debug("GAME RESET DUE TO FALLEN WORDS")

    def _reset_game_state(self):
        try:
            self.correct_words_typed = 0
            self.incorrect_words_typed = 0
            self.gui.input_textbox.delete("1.0", "end")
            self.gui.word_animation_box.reset_game()
            self.gui.input_textbox.bind("<KeyRelease>", self.on_key_press)
            self.running = False
            self.game_reset = True
            self.logger.debug("RESET GAME STATS")

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
