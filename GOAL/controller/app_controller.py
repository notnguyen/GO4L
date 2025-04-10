import pickle
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from config.config import ai_model


class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.match_id_map = {}
        self.load_matches()

        self.view.played_listbox.bind("<<ListboxSelect>>", self.on_played_match_selected)
        self.view.predict_button.config(state=tk.DISABLED)

    def load_matches(self):
        played = self.model.get_matches()

        for idx, match in enumerate(played):
            self.view.played_listbox.insert(tk.END, match['text'])
            self.match_id_map[idx] = match['id']

    def on_played_match_selected(self, event):
        selection = event.widget.curselection()
        if not selection:
            return
        index = selection[0]
        match_id = self.match_id_map.get(index)
        if match_id:
            detail = self.model.get_match_detail(match_id)
            self.show_match_detail(detail)
            self.view.predict_button.config(state=tk.NORMAL)

    def on_predict_match_selected(self):
        selection = self.view.played_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        match_id = self.match_id_map.get(index)
        if match_id:
            detail = self.model.get_match_detail(match_id)
            self.predict_match_result(detail)

    def show_match_detail(self, match):

        home_stats = match['homeTeam'].get('statistics', {})
        away_stats = match['awayTeam'].get('statistics', {})
        home_lineup = ', '.join([str(p['id']) for p in match['homeTeam'].get('lineup', [])])
        away_lineup = ', '.join([str(p['id']) for p in match['awayTeam'].get('lineup', [])])

        match_id = match['id']
        season = match['season']['startDate']
        area = match['area']['name']
        league = match['competition']['name']
        date = match['utcDate']
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        matchday = match.get('matchday', 'Unknown')
        venue = match.get('venue', 'Unknown')
        attendance = match.get('attendance', 0)
        score = match['score']['fullTime']
        home_coach = home_stats.get('coach', {}).get('name', 'Unknown')
        home_formation = home_stats.get('formation', 'Unknown')
        home_possession = home_stats.get('ball_possession', 0)
        home_shots = home_stats.get('shots', 0)
        home_shots_on_goal = home_stats.get('shots_on_goal', 0)
        home_shots_off_goal = home_stats.get('shots_off_goal', 0)
        home_free_kicks = home_stats.get('free_kicks', 0)
        home_goal_kicks = home_stats.get('goal_kicks', 0)
        home_offsides = home_stats.get('offsides', 0)
        home_saves = home_stats.get('saves', 0)
        home_throw_ins = home_stats.get('throw_ins', 0)
        home_fouls = home_stats.get('fouls', 0)
        home_yellow_cards = home_stats.get('yellow_cards', 0)
        home_red_cards = home_stats.get('red_cards', 0)
        away_coach = away_stats.get('coach', {}).get('name', 'Unknown')
        away_formation = away_stats.get('formation', 'Unknown')
        away_possession = away_stats.get('ball_possession', 0)
        away_shots = away_stats.get('shots', 0)
        away_shots_on_goal = away_stats.get('shots_on_goal', 0)
        away_shots_off_goal = away_stats.get('shots_off_goal', 0)
        away_free_kicks = away_stats.get('free_kicks', 0)
        away_goal_kicks = away_stats.get('goal_kicks', 0)
        away_offsides = away_stats.get('offsides', 0)
        away_saves = away_stats.get('saves', 0)
        away_throw_ins = away_stats.get('throw_ins', 0)
        away_fouls = away_stats.get('fouls', 0)
        away_yellow_cards = away_stats.get('yellow_cards', 0)
        away_red_cards = away_stats.get('red_cards', 0)

        detail_info = (
            f"ID: {match_id}\n"
            f"Season: {season}\n"
            f"Area: {area}\n"
            f"League: {league}\n"
            f"Date: {date}\n"
            f"Match: {home_team} vs {away_team}\n"
            f"Matchday: {matchday}\n"
            f"Venue: {venue}\n"
            f"Attendance: {attendance}\n"
            f"Home Lineup: {home_lineup}\n"
            f"Away Lineup: {away_lineup}\n"
            f"Coach: {home_coach} vs {away_coach}\n"
            f"Home Formation: {home_formation}\n"
            f"Away Formation: {away_formation}\n"
            f"Possession: {home_possession} : {away_possession}\n"
            f"Shots: {home_shots} : {away_shots}\n"
            f"Shots_on_goal: {home_shots_on_goal} : {away_shots_on_goal}\n"
            f"Shots_off_goal: {home_shots_off_goal} : {away_shots_off_goal}\n"
            f"Free_kicks: {home_free_kicks} : {away_free_kicks}\n"
            f"Goal_kicks: {home_goal_kicks} : {away_goal_kicks}\n"
            f"Offsides: {home_offsides} : {away_offsides}\n"
            f"Saves: {home_saves} : {away_saves}\n"
            f"Throw_ins: {home_throw_ins} : {away_throw_ins}\n"
            f"Fouls: {home_fouls} : {away_fouls}\n"
            f"Yellow_cards: {home_yellow_cards} : {away_yellow_cards}\n"
            f"Red_cards: {home_red_cards} : {away_red_cards}\n"
            f"Score: {score['home']} : {score['away']}\n"
        )
        messagebox.showinfo("Match Details", detail_info)


    def predict_match_result(self, match):
        home_stats = match['homeTeam'].get('statistics', {})
        away_stats = match['awayTeam'].get('statistics', {})

        features = [
            home_stats.get('ball_possession', 0),
            away_stats.get('ball_possession', 0),
            home_stats.get('shots', 0),
            away_stats.get('shots', 0),
            home_stats.get('shots_on_goal', 0),
            away_stats.get('shots_on_goal', 0),
            home_stats.get('shots_off_goal', 0),
            away_stats.get('shots_off_goal', 0),
            home_stats.get('fouls', 0),
            away_stats.get('fouls', 0),
            home_stats.get('yellow_cards', 0),
            away_stats.get('yellow_cards', 0),
            home_stats.get('red_cards', 0),
            away_stats.get('red_cards', 0),
            home_stats.get('saves', 0),
            away_stats.get('saves', 0),
            home_stats.get('goal_kicks', 0),
            away_stats.get('goal_kicks', 0),
            home_stats.get('throw_ins', 0),
            away_stats.get('throw_ins', 0),
            home_stats.get('offsides', 0),
            away_stats.get('offsides', 0),
            home_stats.get('free_kicks', 0),
            away_stats.get('free_kicks', 0),
        ]

        feature_names = [
            "home_possession", "away_possession",
            "home_shots", "away_shots",
            "home_shots_on_goal", "away_shots_on_goal",
            "home_shots_off_goal", "away_shots_off_goal",
            "home_fouls", "away_fouls",
            "home_yellow_cards", "away_yellow_cards",
            "home_red_cards", "away_red_cards",
            "home_saves", "away_saves",
            "home_goal_kicks", "away_goal_kicks",
            "home_throw_ins", "away_throw_ins",
            "home_offsides", "away_offsides",
            "home_free_kicks", "away_free_kicks"
        ]

        df = pd.DataFrame([features], columns=feature_names)

        with open(ai_model, 'rb') as f:
            logreg = pickle.load(f)

        prediction = logreg.predict(df)[0]

        if prediction == 1:
            predicted_result = "Home Win"
        elif prediction == 2:
            predicted_result = "Draw"
        elif prediction == 0:
            predicted_result = "Away Win"
        else:
            predicted_result = "Unknown"

        messagebox.showinfo("Match Prediction", f"Predicted Result: {predicted_result}")


