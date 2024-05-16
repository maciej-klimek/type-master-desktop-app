import tkinter as tk
from tkinter import ttk

root = tk.Tk()
buttons = [None] * 7


def del_button():
    for i in range(5, 7):
        buttons[i].destroy()


f1 = tk.Frame(root)
for i in range(6, -1, -1):
    buttons[i] = ttk.Button(f1, text=f"{i}")
    buttons[i].pack(side=tk.RIGHT)
f2 = tk.Frame(root)
button_del = ttk.Button(f2, text='Delete', command=del_button)
button_del.pack(side=tk.LEFT)
f1.pack(fill=tk.X, expand=True)
f2.pack(fill=tk.X, expand=True)
root.mainloop()
