import random
from word_reader import read_words
import tkinter as tk



word_list=read_words('words.txt')
canvas_width = 800
canvas_height = 600
font_size = 30
canvas = tk.Canvas(root, width=canvas_width,
                   height=canvas_height, bg='#242424')
canvas.pack()

def generate_word():
    global word_labels, word_positions, generated_words
    print(generated_words)
    word = random.choice(word_list)

    while word in generated_words:
        if len(word_list) == len(generated_words):
            generated_words = []
        word = random.choice(word_list)
    generated_words.append(word)
    x_pos = random.randint(-500, -100)
    y_pos = random.randint(30, canvas_height - 30)
    word_label = canvas.create_text(x_pos, y_pos, text=word, fill='white', font=(
        'Cascadia mono', font_size), anchor='w')
    word_labels.append(word_label)
    word_positions.append((x_pos, y_pos))
    canvas.after(1000, generate_word)

def slide_words_through_canvas():
    global word_labels, word_positions
    for i, label_id in enumerate(word_labels):
        canvas.move(label_id, 0.2, 0)  # Move words slowly to the right
        x, _ = canvas.coords(label_id)
        if x > canvas_width:  # If word reaches the right side
            canvas.delete(label_id)  # Remove the word label from the canvas
            word_labels.pop(i)  # Remove the label from the list
            break