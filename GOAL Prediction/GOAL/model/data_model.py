class CompetitionModel:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_competition_names(self):
        data = self.api_client.get_competitions()
        return [comp['name'] for comp in data.get('competitions', [])]

class SerieAModel:
    def __init__(self, api_client):
        self.api_client = api_client
        self.raw_data = self.api_client.get_serie_a_matches()

    def get_match_groups(self):
        played = []
        upcoming = []

        for match in self.raw_data.get('matches', []):
            home = match['homeTeam']['name']
            away = match['awayTeam']['name']
            date = match['utcDate'][:10]
            score = match['score']['fullTime']

            if score['home'] is not None and score['away'] is not None:
                result = f"{home} {score['home']} : {score['away']} {away} ({date})"
                played.append(result)
            else:
                upcoming.append(f"{home} vs {away} ({date})")

        return played, upcoming

    def get_played_match_features(self):
        # Získání stejné featury jako ve tvém modelu
        features_list = []
        for match in self.raw_data.get("matches", []):
            score = match["score"]["fullTime"]
            if score["home"] is None:
                continue

            # Příkladná data – reálně musíš sem napojit skutečné statistiky
            # Tyto hodnoty musíš vytáhnout z jiného zdroje nebo upravit API clienta
            features = [
                50, 50, 10, 8, 5, 3, 5, 5,
                12, 14, 2, 3, 0, 1, 4, 5,
                6, 5, 10, 12, 3, 4
            ]
            features_list.append(features)
        return features_list

