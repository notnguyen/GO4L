
import tkinter as tk
from tkinter import ttk
class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.title("Serie A Matches + Prediction")
        self.geometry("700x400")

        ttk.Label(self, text="Matches:").pack(pady=5)
        self.played_listbox = tk.Listbox(self, width=100, height=15)
        self.played_listbox.pack(pady=5)

        self.predict_button = ttk.Button(self, text="Predict Match Result", command=self.predict_match)
        self.predict_button.pack(pady=10)

    def predict_match(self):
        if self.controller:
            self.controller.on_predict_match_selected()
