import customtkinter as ctk
import tkinter as tk
import random
import logging
import sqlite3
from config import WORDS_PATH

logging.basicConfig(level=logging.DEBUG)


class AnimationBox(ctk.CTkLabel):
    def __init__(self, root, word_typing_mode_instance, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.logger = logging.getLogger(__name__)

        self.root = root
        self.word_typing_mode = word_typing_mode_instance
        self.canvas_width = 900
        self.canvas_height = 520
        self.font_size = 20
        self.game_started = False

        self.word_moving_speed = 0.07
        self.word_generating_speed = 1500
        self.max_num_of_fallen_words = 5

        self.canvas = tk.Canvas(self.root, width=self.canvas_width,
                                height=self.canvas_height, bg='#242424')

        self.canvas.pack(pady=[0, 20])

        self.word_labels = []
        self.word_positions = []
        self.generated_words = []
        self.words_fallen = 0

        self.word_list = self.read_words(WORDS_PATH)

    def start_game(self):
        if self.game_started:
            return

        self.game_started = True
        self.generate_words()
        self.slide_words_through_canvas()

    def generate_words(self):
        if not self.game_started:
            return
        word = random.choice(self.word_list)

        while word in self.generated_words:
            if len(self.word_list) == len(self.generated_words):
                self.generated_words = []
            word = random.choice(self.word_list)
        self.generated_words.append(word)
        x_pos = random.randint(50, self.canvas_width - 100)
        y_pos = -50
        word_label = self.canvas.create_text(x_pos, y_pos, text=word, fill='white', font=(
            'Cascadia mono', self.font_size), anchor='w')
        self.word_labels.append(word_label)
        self.word_positions.append((x_pos, y_pos))
        self.canvas.after(self.word_generating_speed, self.generate_words)
        # self.logger.debug(self.generated_words)

    def slide_words_through_canvas(self):
        if not self.game_started:
            return
        for i, label_id in enumerate(self.word_labels):
            self.canvas.move(label_id, 0, self.word_moving_speed)
            _, y = self.canvas.coords(label_id)
            if y > self.canvas_height:
                self.canvas.delete(label_id)
                self.word_labels.pop(i)
                self.words_fallen += 1
                if self.words_fallen >= self.max_num_of_fallen_words:
                    self.reset_game_state()
                    self.word_typing_mode.end_game()
                    break
        self.canvas.after(1, self.slide_words_through_canvas)

    def remove_word_from_canvas(self, word):
        for i, label_id in enumerate(self.word_labels):
            if self.canvas.itemcget(label_id, "text") == word:
                self.canvas.delete(label_id)
                self.word_labels.pop(i)
                break

    def reset_game_state(self):
        self.logger.debug("RESET GUI")
        self.reset_canvas()
        self.words_fallen = 0
        self.word_moving_speed = 0.07
        self.word_generating_speed = 1500
        self.game_started = False

    def reset_canvas(self):
        for label_id in self.word_labels:
            self.canvas.delete(label_id)
        self.word_labels.clear()
        self.generated_words.clear()

    def read_words(db_path):
        words = []
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT word FROM words")
            rows = cursor.fetchall()
            words = [row[0] for row in rows]
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
        except Exception as e:
            logging.error(f"Exception in read_words: {e}")
        finally:
            if conn:
                conn.close()
        return words
