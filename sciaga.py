import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import sqlite3
import os

class SQLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ściąga wykonana przez: Ksawery Kamiński")
        self.create_widgets()

    def create_widgets(self):
        self.display_button = ttk.Button(self.root, text="Wyświetl Ściągę", command=self.display_cheat_sheet)
        self.display_button.pack(pady=5)
        self.clear_button = ttk.Button(self.root, text="Wyczyść", command=self.clear_text_area, state=tk.DISABLED)
        self.clear_button.pack(pady=5)
        self.save_button = ttk.Button(self.root, text="Zapisz do Pliku", command=self.save_to_file, state=tk.DISABLED)
        self.save_button.pack(pady=5)
        self.exit_button = ttk.Button(self.root, text="Wyjdź", command=self.root.destroy)
        self.exit_button.pack(pady=5)
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack(padx=10, pady=10)
        self.text_area.config(state=tk.DISABLED)

    def display_cheat_sheet(self):
        if not os.path.exists('sciaga.sql'):
            self.update_text_area("Nie znaleziono pliku ściągi.")
            return

        try:
            conn = sqlite3.connect(':memory:')
            conn.text_factory = lambda b: b.decode(errors='ignore')
            cursor = conn.cursor()

            with open('sciaga.sql', 'r', encoding='utf-8') as file:
                sql_script = file.read()
                cursor.executescript(sql_script)

            cursor.execute('SELECT sciaga_content FROM sciaga')
            rows = cursor.fetchall()
            self.update_text_area('\n'.join(row[0] for row in rows))

            self.display_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)

        except Exception as e:
            self.update_text_area(f"Błąd: {e}")

        finally:
            cursor.close()
            conn.close()

    def clear_text_area(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)

        self.display_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Pliki tekstowe", ".txt"), ("Wszystkie pliki", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_area.get("1.0", tk.END))
                messagebox.showinfo("Sukces", "Plik został zapisany pomyślnie.")
            except Exception as e:
                messagebox.showerror("Błąd", f"Błąd podczas zapisywania pliku: {e}")

    def update_text_area(self, content):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, content)
        self.text_area.config(state=tk.DISABLED)

root = tk.Tk()
app = SQLApp(root)
root.mainloop()
