import time
from ui.ui_main import GUI
import threading


class SentenceTest():
    def __init__(self):
        self.gui = GUI()
        self.gui.reset_button.setcommand = self.reset

        self.correct_text = self.gui.text_label.cget("text")
        self.current_index = 0
        self.running = False

        self.gui.input_entry.bind("<KeyPress>", self.start)
        self.gui.run()

    def start(self, event):

        typed_text = self.gui.input_entry.get()
        text_data = self.gui.text_label.cget("text")

        # Get the current character being typed
        typed_char = event.char.lower()  # Convert to lowercase for case insensitivity

        if not self.running:
            self.running = True
            # Clear the input field when starting
            self.gui.input_entry.delete(0, "end")
            t = threading.Thread(target=self.time_thread)
            t.start()

        # Check if the typed character matches the correct character at the current index
        if typed_char == self.correct_text[self.current_index].lower():
            self.gui.input_entry.configure(text_color="white")
            self.current_index += 1

            # If all characters have been correctly typed
            if self.current_index >= len(self.correct_text) + 1:
                self.running = False
                # Unbind further keypresses
                self.gui.input_entry.unbind("<Key>")
                self.gui.input_entry.configure(
                    state="disabled")  # Disable input field
        else:
            self.gui.input_entry.configure(text_color="red")
            return "break"

    def time_thread(self):
        counter = 0
        while self.running:
            time.sleep(0.1)
            counter += 0.1
            cps = self.current_index / counter
            cpm = cps * 60
            self.gui.speed_label.configure(
                text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM")

    def reset(self):
        self.running = False
        self.current_index = 0
        self.gui.input_entry.configure(state="normal")
        self.gui.input_entry.delete(0, "end")
        self.gui.input_entry.bind("<KeyPress>", self.start)
        self.gui.input_entry.focus()


SentenceTest()
