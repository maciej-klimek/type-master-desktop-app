import threading
import logging
import random
import time
from ui.ui_main import GUI

logging.basicConfig(level=logging.DEBUG)

SPECIAL_KEYS = {
    "Shift_L": "Left Shift",
    "Shift_R": "Right Shift",
    "Control_L": "Left Ctrl",
    "Control_R": "Right Ctrl",
    "Alt_L": "Left Alt",
    "Alt_R": "Right Alt",
    "Caps_Lock": "Caps Lock"
}


class MeasureAccuracyMode():
    def __init__(self):

        self.logger = logging.getLogger(__name__)
        self.gui = GUI()

        self.running = False
        self.chars_typed = 0

        self.get_new_text()

        self.gui.input_textbox.bind("<Button-1>", self.on_start)
        self.gui.reset_button.bind("<Button-1>", self.on_reset)
        self.gui.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.gui.run()

    def get_new_text(self, event=None):
        self.text_data = open("text_data.txt", "r").read().split("\n")
        self.correct_text = random.choice(self.text_data)
        self.hidden_correct_text = "".join(
            char if char == " " else "*" for char in self.correct_text
        )
        self.gui.text_label.configure(text=self.hidden_correct_text)

    def on_start(self, event=None):
        self.gui.input_textbox.bind("<Key>", self.on_key_press)
        self.gui.text_label.configure(text=self.correct_text)
        self.logger.debug("start")

        if not self.running:
            self.running = True
            self.writting_thread = threading.Thread(
                target=self.calculate_stats)
            self.writting_thread.daemon = True
            self.writting_thread.start()

    # DODAC ACCURACY MEASURE (WBUDOWANA LIB TO POROWNYWANIA STRINGOW)

    def on_key_press(self, event):
        key_code = event.keysym
        if key_code == "Return":
            self.running = False
            self.gui.input_textbox.unbind("<KeyPress>")
            self.gui.input_textbox.configure(state="disabled")
            self.logger.debug("enter pressed")
        elif key_code == "BackSpace":
            self.logger.debug("backspace pressed")
            if self.chars_typed > 0:
                self.chars_typed -= 1
                self.logger.debug("backspace pressed and deleted a char")

        elif key_code in SPECIAL_KEYS:
            self.logger.debug("special key pressed")

        else:
            self.chars_typed += 1

        self.logger.debug(self.chars_typed)

    def calculate_stats(self):
        counter = 0
        while self.running:
            time.sleep(0.05)
            counter += 0.1
            cps = self.chars_typed / counter
            cpm = cps * 60
            self.gui.speed_label.configure(
                text=f"CPS: {cps:.2f}\nCPM: {cpm:.2f}")

    def on_reset(self, event=None):
        self.get_new_text()
        self.chars_typed = 0
        self.gui.input_textbox.unbind("<Key>")
        self.gui.input_textbox.delete("0.0", "end")
        self.gui.input_textbox.configure(text_color="white")
        self.logger.debug("reset")

    def on_closing(self):
        self.running = False
        self.gui.root.destroy()
        self.logger.debug("closing")


if __name__ == "__main__":
    MeasureAccuracyMode()
