import tkinter as tk
import random


def slide_words_through_canvas():
    global word_labels, word_positions
    for i, label_id in enumerate(word_labels):
        canvas.move(label_id, 0, 0.2)  # Move words slowly downwards
        _, y = canvas.coords(label_id)
        if y > canvas_height:  # If word reaches the bottom
            canvas.delete(label_id)  # Remove the word label from the canvas
            word_labels.pop(i)  # Remove the label from the list
            break

    canvas.after(1, slide_words_through_canvas)


def generate_word():
    global word_labels, word_positions, generated_words
    word = random.choice(word_list)

    while word in generated_words:
        if len(word_list) == len(generated_words):
            generated_words = []
        word = random.choice(word_list)
    generated_words.append(word)
    # Start words within canvas width
    x_pos = random.randint(100, canvas_width - 200)
    # Start words outside the top of the canvas
    y_pos = random.randint(-500, -100)
    word_label = canvas.create_text(x_pos, y_pos, text=word, fill='white', font=(
        'Cascadia mono', font_size), anchor='w')
    word_labels.append(word_label)
    word_positions.append((x_pos, y_pos))
    # Recursive call to generate words every 500 milliseconds
    canvas.after(1000, generate_word)


def read_words(filename):
    with open(filename, 'r') as file:
        words = file.readlines()
    return [word.strip() for word in words]


def is_colliding(x1, y1, x2, y2):
    if abs(x1 - x2) < 100 and abs(y1 - y2) < 30:

        return True
    else:
        return False


root = tk.Tk()
root.title("Word Flow")
root.configure(bg='black')

word_list = read_words('gui/words.txt')

canvas_width = 800
canvas_height = 600
font_size = 30

canvas = tk.Canvas(root, width=canvas_width,
                   height=canvas_height, bg='#242424')
canvas.pack()

word_labels = []
word_positions = []
generated_words = []
slide_words_through_canvas()  # Start moving words

generate_word()  # Start generating words

root.mainloop()
