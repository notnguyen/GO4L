import requests
import json
from config.config import base_url, headers

class FootballAPIClient:

    def get_serie_a_matches(self):
        url = f"{base_url}competitions/SA/matches"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("matches", [])

    def get_match_details(self, match_id):
        url = f"{base_url}matches/{match_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

