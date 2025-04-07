import requests
import json
from config.config import key, url

class FootballAPIClient:
    base_url = url

    def __init__(self):
        self.headers = {"X-Auth-Token": key}
    def get_serie_a_matches(self):
        uri = f"{base_url}competitions/SA/matches"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("matches", [])

    def get_match_details(self, match_id):
        uri = f"{base_url}matches/{match_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

