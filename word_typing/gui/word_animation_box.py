import customtkinter as ctk
import tkinter as tk
import random
from config import WORDS_PATH

class WordAnimationBox(ctk.CTkLabel):
    def __init__(self, root, canvas_width=700, canvas_height=500, font_size=30, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.font_size = font_size
        self.game_started = False

        self.canvas = tk.Canvas(self.root, width=self.canvas_width,
                                height=self.canvas_height, bg='#242424')

        self.canvas.pack()

        self.word_labels = []
        self.word_positions = []
        self.generated_words = []
        self.words_fallen = 0

        self.word_list = self.read_words(WORDS_PATH)

    def start_game(self):
        if self.game_started:
            return

        self.game_started = True
        self.generate_word()
        self.slide_words_through_canvas()

    def generate_word(self):
        if not self.game_started:
            return
        word = random.choice(self.word_list)

        while word in self.generated_words:
            if len(self.word_list) == len(self.generated_words):
                self.generated_words = []
            word = random.choice(self.word_list)
        self.generated_words.append(word)
        # Start words within canvas width
        x_pos = random.randint(100, self.canvas_width - 200)
        # Start words outside the top of the canvas
        y_pos = random.randint(-500, -100)
        word_label = self.canvas.create_text(x_pos, y_pos, text=word, fill='white', font=(
            'Cascadia mono', self.font_size), anchor='w')
        self.word_labels.append(word_label)
        self.word_positions.append((x_pos, y_pos))
        self.canvas.after(1000, self.generate_word)

    def slide_words_through_canvas(self):
        if not self.game_started:
            return
        for i, label_id in enumerate(self.word_labels):
            self.canvas.move(label_id, 0, 0.1)  # Move words slowly downwards
            _, y = self.canvas.coords(label_id)
            if y > self.canvas_height:  # If word reaches the bottom
                # Remove the word label from the canvas
                self.canvas.delete(label_id)
                self.word_labels.pop(i)  # Remove the label from the list
                self.words_fallen += 1
                if self.words_fallen >= 5:
                    self.reset_game()
                    break
        self.canvas.after(1, self.slide_words_through_canvas)

    def remove_word_from_canvas(self, word):
        for i, label_id in enumerate(self.word_labels):
            if self.canvas.itemcget(label_id, "text") == word:
                self.canvas.delete(label_id)
                self.word_labels.pop(i)
                break

    def reset_game(self):
        self.reset_words()
        self.words_fallen = 0
        self.game_started = False

    def reset_words(self):
        for label_id in self.word_labels:
            self.canvas.delete(label_id)
        self.word_labels.clear()
        self.generated_words.clear()

    @staticmethod
    def read_words(filename):
        with open(filename, 'r') as file:
            words = file.readlines()
        return [word.strip() for word in words]

    def is_colliding(self, x1, y1, x2, y2):
        return abs(x1 - x2) < 100 and abs(y1 - y2) < 30
