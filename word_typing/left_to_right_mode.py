import random
import time
import logging
import threading
from gui.gui_main_mode1 import GUI
from word_typing.animation_left_to_right import slide_words_through_canvas, generate_word, read_words

logging.basicConfig(level=logging.DEBUG)

class LeftToRightMode():
    def __init__(self):

        self.logger = logging.getLogger(__name__)
        self.gui = GUI()

        self.running = False
        self.correct_chars_typed = 0
        self.incorrect_chars_typed = 0
        self.current_typing_index = 0

        self.start_animation()

        self.gui.input_textbox.bind("<Button-1>", self.start_animation())
        self.gui.reset_button.bind("<Button-1>", self.reset())
        self.gui.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.gui.run()

    def start_animation(self):
        slide_words_through_canvas()
        generate_word()

    def reset(self):
        self.start_animation()
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
    LeftToRightMode()