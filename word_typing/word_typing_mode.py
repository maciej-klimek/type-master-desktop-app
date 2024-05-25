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
        self.words_for_next_level = 20
        self.level = 1

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
        if input_word in self.gui.word_animation_box.generated_words:
            self.gui.word_animation_box.generated_words.remove(input_word)
            self.gui.input_textbox.delete("1.0", "end")
            self.correct_words_typed += 1
            self.gui.word_animation_box.remove_word_from_canvas(input_word)

    def update_level(self):
        if self.correct_words_typed >= self.words_for_next_level:
            self.level += 1
            self.words_for_next_level += 20
            self.change_background_color()
            self.logger.debug(f"LEVEL UP! New Level: {self.level}")

        self.update_speed_label()

    def change_background_color(self):
        level_colors = {
            1: '#71c788',  # Green
            2: '#6699FF',  # Blue
            3: '#FFFF66',  # Yellow
            4: '#FFB266',  # Orange
            5: '#FF6666'  # Red
        }
        new_color = level_colors.get(self.level, '#71c788')
        self.gui.speed_label.configure(fg_color=new_color)

    def on_reset(self, event=None):
        self._reset_game_state()
        self.gui.input_textbox.bind("<Return>", self.on_start)
        self.gui.input_textbox.unbind("<KeyRelease>")
        self.gui.speed_label.configure(text="Level: 1 \nCorrect words: 0\nNext level: 0")  # Reset speed label
        self.gui.speed_label.configure(fg_color='#71c788')
        self.logger.debug("RESET")

    def update_speed_label(self):
        self.gui.speed_label.configure(
            text=f"Level: {self.level} \nCorrect words: {self.correct_words_typed}\nNext level: {self.words_for_next_level}")

    def reset_game_due_to_fallen_words(self):
        self._reset_game_state()
        self.logger.debug("GAME RESET DUE TO FALLEN WORDS")

    def _reset_game_state(self):
        try:
            self.correct_words_typed = 0
            self.incorrect_words_typed = 0
            self.gui.input_textbox.unbind("<KeyRelease>")
            self.gui.input_textbox.delete("1.0", "end")
            self.gui.word_animation_box.reset_words()
            self.gui.input_textbox.bind("<KeyRelease>", self.on_key_press)
            self.running = False  # Reset the game state
            self.game_reset = True  # Set the game reset flag
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
