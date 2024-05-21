import customtkinter as ctk
from tkinter import messagebox
import sqlite3


def create_connection():
    return sqlite3.connect('words_sentences.db')


def get_all_records(table):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table}')
    records = cursor.fetchall()
    conn.close()
    return records


def add_record(table, entry):
    conn = create_connection()
    cursor = conn.cursor()
    if table == 'sentences':
        cursor.execute('INSERT INTO sentences (sentence) VALUES (?)', (entry,))
    elif table == 'words':
        cursor.execute('INSERT INTO words (word) VALUES (?)', (entry,))
    conn.commit()
    conn.close()


def delete_record(table, record_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {table} WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()


def update_record(table, record_id, new_entry):
    conn = create_connection()
    cursor = conn.cursor()
    if table == 'sentences':
        cursor.execute(
            'UPDATE sentences SET sentence = ? WHERE id = ?', (new_entry, record_id))
    elif table == 'words':
        cursor.execute('UPDATE words SET word = ? WHERE id = ?',
                       (new_entry, record_id))
    conn.commit()
    conn.close()


class CTkInputDialog(ctk.CTkToplevel):
    def __init__(self, master=None, title="Input", prompt=""):
        super().__init__(master)
        self.title(title)
        self.geometry("300x150")

        self.result = None

        self.label = ctk.CTkLabel(self, text=prompt)
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=10)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        self.ok_button = ctk.CTkButton(
            self.button_frame, text="OK", command=self.on_ok)
        self.ok_button.pack(side="left", padx=10)

        self.cancel_button = ctk.CTkButton(
            self.button_frame, text="Cancel", command=self.on_cancel)
        self.cancel_button.pack(side="right", padx=10)

        self.entry.bind("<Return>", lambda event: self.on_ok())
        self.entry.bind("<Escape>", lambda event: self.on_cancel())

    def on_ok(self):
        self.result = self.entry.get()
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()


class DatabaseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Database Manager")
        self.geometry("800x400")

        self.table = ctk.StringVar(value="sentences")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="both",
                        expand=True, padx=10, pady=10)

        self.output_text = ctk.CTkTextbox(left_frame)
        self.output_text.configure(font=("Courier", 12), wrap="word")
        self.output_text.pack(fill="both", expand=True)

        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)

        ctk.CTkLabel(right_frame, text="Select Table:").pack(pady=5)
        ctk.CTkOptionMenu(right_frame, variable=self.table, values=[
                          "sentences", "words"]).pack(pady=5)

        self.view_button = ctk.CTkButton(
            right_frame, text="View Records", command=self.view_records)
        self.view_button.pack(pady=5)

        self.add_button = ctk.CTkButton(
            right_frame, text="Add Record", command=self.add_record)
        self.add_button.pack(pady=5)

        self.edit_button = ctk.CTkButton(
            right_frame, text="Edit Record", command=self.edit_record)
        self.edit_button.pack(pady=5)

        self.delete_button = ctk.CTkButton(
            right_frame, text="Delete Record", command=self.delete_record)
        self.delete_button.pack(pady=5)

    def view_records(self):
        self.output_text.delete(1.0, ctk.END)
        table = self.table.get()
        records = get_all_records(table)
        if records:
            for record in records:
                self.output_text.insert(
                    ctk.END, f"{record[0]}. {record[1]}\n")
        else:
            self.output_text.insert(
                ctk.END, f"No records found in {table} table.")

    def add_record(self):
        table = self.table.get()
        dialog = CTkInputDialog(self, title="Input",
                                prompt=f"Enter new {table[:-1]}:")
        self.wait_window(dialog)
        entry = dialog.result
        if entry:
            add_record(table, entry)
            messagebox.showinfo(
                "Success", f"Record added to {table} table.")
            self.view_records()

    def edit_record(self):
        table = self.table.get()
        dialog = CTkInputDialog(self, title="Input",
                                prompt="Enter record ID to edit:")
        self.wait_window(dialog)
        record_id = dialog.result
        if record_id:
            dialog = CTkInputDialog(
                self, title="Input", prompt=f"Enter new {table[:-1]}:")
            self.wait_window(dialog)
            new_entry = dialog.result
            if new_entry:
                update_record(table, record_id, new_entry)
                messagebox.showinfo("Success", f"Record ID {
                                    record_id} updated.")
                self.view_records()

    def delete_record(self):
        table = self.table.get()
        dialog = CTkInputDialog(self, title="Input",
                                prompt="Enter record ID to delete:")
        self.wait_window(dialog)
        record_id = dialog.result
        if record_id:
            delete_record(table, record_id)
            messagebox.showinfo("Success", f"Record ID {record_id} deleted.")
            self.view_records()


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("green")
    app = DatabaseApp()
    app.mainloop()
