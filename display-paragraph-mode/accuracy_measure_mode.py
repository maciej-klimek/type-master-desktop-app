import time
from ui.ui_main import GUI
import threading


class SentenceTest():
    def __init__(self):
        self.gui = GUI()
        self.gui.reset_button.bind("<Button-1>", self.reset)

        self.correct_text = self.gui.text_label.cget("text")
        self.current_index = 0
        self.running = False

        self.gui.input_entry.bind("<KeyPress>", self.start)
        self.gui.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.gui.run()

    def start(self, event):
        typed_char = event.char.lower()

        if not self.running:
            self.running = True
            self.gui.input_entry.delete(0, "end")
            self.t = threading.Thread(target=self.time_thread)
            self.t.start()

        entry_text = self.gui.input_entry.get()
        self.gui.input_entry.configure(state="normal")
        self.gui.input_entry.delete(0, "end")

        for i, (correct_char, typed_char) in enumerate(zip(self.correct_text, entry_text)):
            if typed_char == correct_char:
                self.gui.input_entry.insert("end", typed_char)
                self.gui.input_entry.tag_add("correct", f"1.{i}", f"1.{i+1}")
                self.gui.input_entry.tag_config("correct", foreground="white")
            else:
                self.gui.input_entry.insert("end", typed_char)
                self.gui.input_entry.tag_add("incorrect", f"1.{i}", f"1.{i+1}")
                self.gui.input_entry.tag_config("incorrect", foreground="red")
        self.gui.input_entry.configure(state="disabled")

    def time_thread(self):
        counter = 0
        while self.running:
            time.sleep(0.1)
            counter += 0.1
            cps = self.current_index / counter
            cpm = cps * 60
            self.gui.speed_label.configure(
                text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM")

    def reset(self, event=None):
        print("resetuje")
        self.running = False
        self.current_index = 0
        self.gui.input_entry.configure(state="normal")
        self.gui.input_entry.delete(0, "end")

    def on_closing(self):
        print("closing")
        self.running = False
        self.gui.root.destroy()


SentenceTest()
