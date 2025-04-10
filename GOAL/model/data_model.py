class SerieAModel:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_matches(self):
        matches = self.api_client.get_serie_a_matches()
        played = []
        for match in matches:
            home = match['homeTeam']['name']
            away = match['awayTeam']['name']
            score = match['score']['fullTime']
            match_entry = {
                'id': match['id'],
                'text': f"{home} vs {away}",
                'played': score['home'] is not None
            }
            if match_entry['played']:
                match_entry['text'] = f"{home} : {away}"
                played.append(match_entry)
        return played

    def get_match_detail(self, match_id):
        detail = self.api_client.get_match_details(match_id)


        return detail


