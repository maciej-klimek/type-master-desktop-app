import tkinter as tk
from gui import create_gui
from word_generator import generate_word

def main():
    root = tk.Tk()
    root.title("Word Flow")
    root.configure(bg='black')

    create_gui(root)
    generate_word(root)

    root.mainloop()

if __name__ == "__main__":
    main()