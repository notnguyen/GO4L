import pickle

class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.predict_callback = self.predict_match
        self.played_matches_data = []  # Uložíme si data k zápasům

        self.update_view()

    def update_view(self):
        played, upcoming = self.model.get_match_groups()
        self.view.update_matches(played, upcoming)
        self.played_matches_data = self.model.get_played_match_features()

    def predict_match(self, index):
        try:
            with open("random_forest_model.pkl", "rb") as f:
                model = pickle.load(f)
        except FileNotFoundError:
            return "Model nenalezen."

        features = self.played_matches_data[index]
        prediction = model.predict([features])[0]

        if prediction == "W":
            return "🏠 Výhra domácích"
        elif prediction == "L":
            return "🏠 Prohra domácích"
        elif prediction == "D":
            return "🤝 Remíza"
        else:
            return f"Neznámý výsledek: {prediction}"
