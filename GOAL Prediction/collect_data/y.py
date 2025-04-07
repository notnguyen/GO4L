import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import threading  
import pickle

API_KEY = '9be9843eb46e4df7b8bb5b8ca44adb00'
HEADERS = {'X-Auth-Token': API_KEY}
BASE_URL = 'https://api.football-data.org/v4/'

class FootballAPIClient:
    def get_serie_a_matches(self):
        url = f"{BASE_URL}competitions/SA/matches"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get("matches", [])

    def get_match_details(self, match_id):
        url = f"{BASE_URL}matches/{match_id}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()

class SerieAModel:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_match_groups(self):
        matches = self.api_client.get_serie_a_matches()
        played, upcoming = [], []
        for match in matches:
            home = match['homeTeam']['name']
            away = match['awayTeam']['name']
            date = match['utcDate'][:10]
            score = match['score']['fullTime']
            match_entry = {
                'id': match['id'],
                'text': f"{home} vs {away} ({date})",
                'played': score['home'] is not None
            }
            if match_entry['played']:
                match_entry['text'] = f"{home} {score['home']} : {score['away']} {away} ({date})"
                played.append(match_entry)
            else:
                upcoming.append(match_entry)
        return played, upcoming

    def get_match_detail(self, match_id):
        return self.api_client.get_match_details(match_id)

class MainView(tk.Tk):



# Načítání modelu
    with open('random_forest_model.pkl', 'rb') as f:
        rf = pickle.load(f)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Serie A Matches Viewer")
        self.geometry("1000x700")

        ttk.Label(self, text="Played Matches:").pack(pady=5)
        self.played_listbox = tk.Listbox(self, width=120, height=10)
        self.played_listbox.pack(pady=5)
        self.played_listbox.bind('<Double-1>', self.on_played_select)

        ttk.Label(self, text="Upcoming Matches:").pack(pady=5)
        self.upcoming_listbox = tk.Listbox(self, width=120, height=10)
        self.upcoming_listbox.pack(pady=5)
        self.upcoming_listbox.bind('<Double-1>', self.on_upcoming_select)

        # Přidání tlačítka pro predikci
        self.predict_button = ttk.Button(self, text="Predict Match Outcome", command=self.predict_match)
        self.predict_button.pack(pady=10)

    def update_matches(self, played, upcoming):
        self.played_listbox.delete(0, tk.END)
        self.upcoming_listbox.delete(0, tk.END)
        self.played_data = played
        self.upcoming_data = upcoming

        for match in played:
            self.played_listbox.insert(tk.END, match['text'])
        for match in upcoming:
            self.upcoming_listbox.insert(tk.END, match['text'])

    def on_played_select(self, event):
        idx = self.played_listbox.curselection()
        if idx:
            match = self.played_data[idx[0]]
            self.controller.show_match_detail(match['id'])

    def on_upcoming_select(self, event):
        idx = self.upcoming_listbox.curselection()
        if idx:
            match = self.upcoming_data[idx[0]]
            self.controller.show_match_detail(match['id'])

    def show_detail_window(self, data):
        detail_win = tk.Toplevel(self)
        detail_win.title("Match Details")
        detail_win.geometry("900x700")

        output = scrolledtext.ScrolledText(detail_win, wrap=tk.WORD, width=120, height=40)
        output.pack(padx=10, pady=10)

        try:
            home_stats = data['homeTeam'].get('statistics', {})
            away_stats = data['awayTeam'].get('statistics', {})
            home_lineup = ', '.join([str(p['id']) for p in data['homeTeam'].get('lineup', [])])
            away_lineup = ', '.join([str(p['id']) for p in data['awayTeam'].get('lineup', [])])

            info = {
                "match_id": data['id'],
                "season": data['season']['startDate'],
                "area": data['area']['name'],
                "league": data['competition']['name'],
                "date": data['utcDate'],
                "matchday": data.get('matchday', 'Unknown'),
                "venue": data.get('venue', 'Unknown'),
                "attendance": data.get('attendance', 0),
                "home_team": data['homeTeam']['name'],
                "away_team": data['awayTeam']['name'],
                "home_coach": data['homeTeam'].get('coach', {}).get('name', 'Unknown'),
                "away_coach": data['awayTeam'].get('coach', {}).get('name', 'Unknown'),
                "home_formation": data['homeTeam'].get('formation', 'Unknown'),
                "away_formation": data['awayTeam'].get('formation', 'Unknown'),
                "home_lineup": home_lineup,
                "away_lineup": away_lineup,
                "home_possession": home_stats.get('ball_possession', 0),
                "away_possession": away_stats.get('ball_possession', 0),
                "home_shots": home_stats.get('shots', 0),
                "away_shots": away_stats.get('shots', 0),
                "home_shots_on_goal": home_stats.get('shots_on_goal', 0),
                "away_shots_on_goal": away_stats.get('shots_on_goal', 0),
                "home_shots_off_goal": home_stats.get('shots_off_goal', 0),
                "away_shots_off_goal": away_stats.get('shots_off_goal', 0),
                "home_free_kicks": home_stats.get('free_kicks', 0),
                "away_free_kicks": away_stats.get('free_kicks', 0),
                "home_goal_kicks": home_stats.get('goal_kicks', 0),
                "away_goal_kicks": away_stats.get('goal_kicks', 0),
                "home_offsides": home_stats.get('offsides', 0),
                "away_offsides": away_stats.get('offsides', 0),
                "home_saves": home_stats.get('saves', 0),
                "away_saves": away_stats.get('saves', 0),
                "home_throw_ins": home_stats.get('throw_ins', 0),
                "away_throw_ins": away_stats.get('throw_ins', 0),
                "home_fouls": home_stats.get('fouls', 0),
                "away_fouls": away_stats.get('fouls', 0),
                "home_yellow_cards": home_stats.get('yellow_cards', 0),
                "away_yellow_cards": away_stats.get('yellow_cards', 0),
                "home_yellow_red_cards": home_stats.get('yellow_red_cards', 0),
                "away_yellow_red_cards": away_stats.get('yellow_red_cards', 0),
                "home_red_cards": home_stats.get('red_cards', 0),
                "away_red_cards": away_stats.get('red_cards', 0),
                "full_time_home": data['score']['fullTime']['home'],
                "full_time_away": data['score']['fullTime']['away'],
                "half_time_home": data['score']['halfTime']['home'],
                "half_time_away": data['score']['halfTime']['away']
            }

            for key, value in info.items():
                output.insert(tk.END, f"{key}: {value}\n")

            # Přidání predikce
            self.prediction_output = ttk.Label(detail_win, text="Prediction: Pending...", font=("Arial", 12))
            self.prediction_output.pack(pady=10)

            self.match_data = info  # Uložení dat pro predikci

        except Exception as e:
            output.insert(tk.END, f"Chyba při zobrazení detailů: {e}")

    def predict_match(self):
      if not hasattr(self, 'match_data'):
          messagebox.showerror("Error", "No match selected for prediction.")
          return

      match = self.match_data
      features = [
          match['home_possession'], match['away_possession'],
          match['home_shots'], match['away_shots'],
          match['home_shots_on_goal'], match['away_shots_on_goal'],
          match['home_shots_off_goal'], match['away_shots_off_goal'],
          match['home_fouls'], match['away_fouls'],
          match['home_yellow_cards'], match['away_yellow_cards'],
          match['home_red_cards'], match['away_red_cards'],
          match['home_saves'], match['away_saves'],
          match['home_goal_kicks'], match['away_goal_kicks'],
          match['home_throw_ins'], match['away_throw_ins'],
          match['home_offsides'], match['away_offsides'],
          match['home_free_kicks'], match['away_free_kicks']
      ]

      prediction = self.rf.predict([features])[0]  # zajišťujeme, že máme pouze jeden výsledek predikce
      predicted_result = ""

      if prediction == 0:
          predicted_result = "Home Win"
      elif prediction == 1:
          predicted_result = "Draw"
      elif prediction == 2:
          predicted_result = "Away Win"

      self.prediction_output.config(text=f"Prediction: {predicted_result}")



class AppController:
    def __init__(self):
        self.api_client = FootballAPIClient()
        self.model = SerieAModel(self.api_client)
        self.view = MainView(self)
        threading.Thread(target=self.update_view).start()

    def update_view(self):
        try:
            played, upcoming = self.model.get_match_groups()
            self.view.update_matches(played, upcoming)
        except Exception as e:
            messagebox.showerror("Error", f"Chyba při načítání zápasů: {e}")

    def show_match_detail(self, match_id):
        def fetch():
            try:
                data = self.model.get_match_detail(match_id)
                self.view.show_detail_window(data)
            except Exception as e:
                messagebox.showerror("Error", f"Chyba při načítání detailu: {e}")
        threading.Thread(target=fetch).start()

if __name__ == '__main__':
    app = AppController()
    app.view.mainloop()
