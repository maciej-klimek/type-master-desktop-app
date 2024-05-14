import customtkinter as ctk
import tkinter as tk
import random

class WordsLabel(ctk.CTkLabel):
    def __init__(self, root, canvas_width=800, canvas_height=600, font_size=30, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.font_size = font_size

        self.canvas = tk.Canvas(self.root, width=self.canvas_width,
                           height=self.canvas_height, bg='#242424')

        self.canvas.pack()

        self.word_labels = []
        self.word_positions = []
        self.generated_words = []

        self.word_list = self.read_words('words.txt')
        self.slide_words_through_canvas()
        self.generate_word()

    def generate_word(self):
        print(self.generated_words)
        word = random.choice(self.word_list)

        while word in self.generated_words:
            if len(self.word_list) == len(self.generated_words):
                self.generated_words = []
            word = random.choice(self.word_list)
        self.generated_words.append(word)
        x_pos = random.randint(-500, -100)
        y_pos = random.randint(30, self.canvas_height - 30)
        word_label = self.canvas.create_text(x_pos, y_pos, text=word, fill='white', font=(
            'Cascadia mono', self.font_size), anchor='w')
        self.word_labels.append(word_label)
        self.word_positions.append((x_pos, y_pos))
        self.canvas.after(1000, self.generate_word)

    def slide_words_through_canvas(self):
        for i, label_id in enumerate(self.word_labels):
            self.canvas.move(label_id, 0.2, 0)  # Move words slowly to the right
            x, _ = self.canvas.coords(label_id)
            if x > self.canvas_width:  # If word reaches the right side
                self.canvas.delete(label_id)  # Remove the word label from the canvas
                self.word_labels.pop(i)  # Remove the label from the list
                break
        self.canvas.after(1, self.slide_words_through_canvas)

    @staticmethod
    def read_words(filename):
        with open(filename, 'r') as file:
            words = file.readlines()
        return [word.strip() for word in words]

    def is_colliding(self, x1, y1, x2, y2):
        return abs(x1 - x2) < 100 and abs(y1 - y2) < 30


root = tk.Tk()
root.title("Word Flow")
root.configure(bg='black')

words_label = WordsLabel(root)

root.mainloop()
