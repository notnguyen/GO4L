import tkinter as tk
from tkinter import ttk

from tkinter import messagebox

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Serie A Matches Viewer + Prediction")
        self.geometry("700x700")

        # Odehrané zápasy
        ttk.Label(self, text="✅ Played Matches:").pack(pady=5)
        self.played_listbox = tk.Listbox(self, width=100, height=15)
        self.played_listbox.pack(pady=5)

        self.predict_button = ttk.Button(self, text="📊 Predikuj výsledek", command=self.predict_selected_match)
        self.predict_button.pack(pady=5)

        # Nadcházející zápasy
        ttk.Label(self, text="⏳ Upcoming Matches:").pack(pady=5)
        self.upcoming_listbox = tk.Listbox(self, width=100, height=10)
        self.upcoming_listbox.pack(pady=5)

        # Tohle přiřadíme později z controlleru
        self.predict_callback = None

    def update_matches(self, played, upcoming):
        self.played_listbox.delete(0, tk.END)
        for match in played:
            self.played_listbox.insert(tk.END, match)

        self.upcoming_listbox.delete(0, tk.END)
        for match in upcoming:
            self.upcoming_listbox.insert(tk.END, match)

    def predict_selected_match(self):
        selection = self.played_listbox.curselection()
        if not selection:
            messagebox.showinfo("Chyba", "Nejprve vyberte zápas.")
            return

        index = selection[0]
        if self.predict_callback:
            result = self.predict_callback(index)
            messagebox.showinfo("Predikce", f"Odhadovaný výsledek: {result}")


