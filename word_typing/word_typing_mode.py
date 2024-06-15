import logging
import threading
from word_typing.gui.gui_main import GUI

logging.basicConfig(level=logging.DEBUG)


class WordTypingMode:
    def __init__(self, parent):
        self.logger = logging.getLogger(__name__)
        self.gui = GUI(parent, self)  # Pass self to GUI

        self.running = False
        self.correct_words_typed = 0
        self.incorrect_words_typed = 0
        self.current_typing_index = 0
        self.game_reset = False

        self.words_for_next_level = 20
        self.increment_of_next_level = 20
        self.level = 1
        self.word_speed_change_factor = 0.03
        self.word_generation_speed_change_factor = 200

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
            game_thread = threading.Thread(
                target=self.gui.animation_box.start_game)
            game_thread.start()
            self.game_reset = False  # Reset the flag
        else:
            self.logger.debug("START")
            self.running = True
            game_thread = threading.Thread(
                target=self.gui.animation_box.start_game)
            game_thread.start()

        self.gui.level_label.configure(
            text="Level: 1 \nCorrect words: 0\nNext level: 0")

    def on_key_press(self, event):
        input_word = self.gui.input_textbox.get("1.0", "end-1c").strip()
        self.logger.debug(input_word)

        is_prefix = any(word.startswith(input_word)
                        for word in self.gui.animation_box.generated_words)

        if is_prefix:
            self.gui.input_textbox.configure(text_color="white")
        else:
            self.gui.input_textbox.configure(text_color="red")
        if input_word in self.gui.animation_box.generated_words:
            self.gui.animation_box.generated_words.remove(input_word)
            self.gui.input_textbox.delete("1.0", "end")
            self.correct_words_typed += 1
            self.gui.animation_box.remove_word_from_canvas(input_word)

        self.update_level()

    def update_level(self):
        if self.correct_words_typed >= self.words_for_next_level:
            if self.level < 7:
                self.level += 1
                self.words_for_next_level += self.increment_of_next_level
                self.change_background_color()
                self.gui.animation_box.word_moving_speed += self.word_speed_change_factor
                self.gui.animation_box.word_generating_speed -= self.word_generation_speed_change_factor
            self.logger.debug(f"LEVEL UP! New Level: {self.level}")

        self.update_level_label()

    def change_background_color(self):
        level_colors = {
            1: '#71c788',  # Green
            2: '#6699FF',  # Blue
            3: '#66FFFF',  # Cyan
            4: '#FFFF66',  # Yellow
            5: '#FFB266',  # Orange
            6: '#FF66FF',  # Magenta
            7: '#FF6666'  # Red
        }
        new_color = level_colors.get(self.level, '#71c788')
        self.gui.level_label.configure(fg_color=new_color)

    def update_level_label(self):
        if self.level == 7:
            self.gui.level_label.configure(
                text=f"Level: {self.level} \nCorrect words: {self.correct_words_typed}\nNext level: MAX LEVEL")
        else:
            self.gui.level_label.configure(
                text=f"Level: {self.level} \nCorrect words: {self.correct_words_typed}\nNext level: {self.words_for_next_level}")

    def on_reset(self, event=None):
        self.gui.input_textbox.bind("<Return>", self.on_start)
        self.gui.input_textbox.unbind("<KeyRelease>")
        self.reset_game_state()
        self.gui.level_label.configure(fg_color='#71c788')
        self.logger.debug("RESET")

    def end_game(self):
        self.reset_game_state()
        self.logger.debug("GAME RESET DUE TO FALLEN WORDS")

    def reset_game_state(self):
        try:
            self.correct_words_typed = 0
            self.incorrect_words_typed = 0
            self.gui.input_textbox.delete("1.0", "end")
            self.gui.animation_box.reset_game_state()
            self.gui.input_textbox.bind("<KeyRelease>", self.on_key_press)
            self.running = False
            self.game_reset = True
            self.gui.level_label.configure(fg_color='#71c788')
            self.gui.health_label.configure(
                text="[   ] [   ] [   ] [   ] [   ]")
            self.level = 1
            self.words_for_next_level = 20
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
