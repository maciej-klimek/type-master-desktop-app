import random
import time
import logging
import threading
from word_typing.gui.gui_main import GUI
from config import WORDS_PATH

logging.basicConfig(level=logging.DEBUG)


class LeftToRightMode():
    def __init__(self, parent):

        self.logger = logging.getLogger(__name__)
        self.gui = GUI(parent)

        self.running = False
        self.correct_chars_typed = 0
        self.incorrect_chars_typed = 0
        self.current_typing_index = 0

        self.gui.input_textbox.bind("<Button-1>")
        self.gui.reset_button.bind("<Button-1>", self.on_reset)

        self.gui.run()

    def on_start(self, event=None):
        self.gui.input_textbox.bind("<Key>", self.on_key_press)
        self.logger.debug("START")

    def on_key_press(self, event):
        typed_char = event.char

    def on_reset(self):
        self.current_typing_index = 0
        self.correct_chars_typed = 0
        self.incorrect_chars_typed = 0
        self.gui.input_textbox.unbind("<Key>")
        self.gui.input_textbox.delete("0.0", "end")
        self.gui.input_textbox.configure(text_color="white")
        self.logger.debug("RESET")

    def on_closing(self):
        self.running = False
        self.gui.root.destroy()
        self.logger.debug("CLOSE")


if __name__ == "__main__":
    LeftToRightMode()
