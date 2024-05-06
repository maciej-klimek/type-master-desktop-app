import tkinter as tk

def create_gui(root, canvas):
    canvas_width = 800
    canvas_height = 600

    canvas - tk.Canvas(root, width=canvas_width,
                       height=canvas_height, bg='#242424')
    canvas.pack()