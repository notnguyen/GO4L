import requests
import json
import csv
import time

LEAGUE_ID = "PD"
SEASON = "2024"
API_KEY = '9be9843eb46e4df7b8bb5b8ca44adb00'
URL = f'http://api.football-data.org/v4/competitions/{LEAGUE_ID}/matches?season={SEASON}'

headers = {'X-Auth-Token': API_KEY}
response = requests.get(URL, headers=headers)

if response.status_code == 200:
    matches_data = response.json()["matches"]

    with open('la_liga_2024_matches_lineup.json', 'w', encoding='utf-8') as json_file:
        json.dump(matches_data, json_file, ensure_ascii=False, indent=4)

    with open('la_liga_2024_matches_lineup.csv', 'w', encoding='utf-8', newline='') as csv_file:
        fieldnames = [
            "match_id", "season", "area", "league", "date", "matchday", "venue", "attendance",
            "home_team", "away_team", "home_coach", "away_coach",
            "home_formation", "away_formation", "home_lineup", "away_lineup",
            "home_possession", "away_possession",
            "home_shots", "away_shots",
            "home_shots_on_goal", "away_shots_on_goal", "home_shots_off_goal", "away_shots_off_goal",
            "home_free_kicks", "away_free_kicks", "home_goal_kicks", "away_goal_kicks",
            "home_offsides", "away_offsides", "home_saves", "away_saves", "home_throw_ins", "away_throw_ins",
            "home_fouls", "away_fouls",
            "home_yellow_cards", "away_yellow_cards", "home_yellow_red_cards", "away_yellow_red_cards",
            "home_red_cards", "away_red_cards",
            "full_time_home", "full_time_away",
            "half_time_home", "half_time_away"
        ]
        
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for i, match in enumerate(matches_data):
            match_id = match["id"]
            match_detail_url = f"http://api.football-data.org/v4/matches/{match_id}"

            match_response = requests.get(match_detail_url, headers=headers)
            
            if match_response.status_code != 200:
                print(f"Chyba při získávání detailu zápasu {match_id}: {match_response.status_code}")
                continue

            data = match_response.json()

            try:
                home_lineup_ids = [player["id"] for player in data["homeTeam"]["lineup"]]
                away_lineup_ids = [player["id"] for player in data["awayTeam"]["lineup"]]

                match_info = {
                    "match_id": data["id"],
                    "season": matches_data[0]["season"]["startDate"],
                    "area" : data["area"]["name"],
                    "league" : data["competition"]["name"],
                    "date": data["utcDate"],
                    "matchday": data["matchday"],
                    "venue": data["venue"] if "venue" in data else "Unknown",
                    "attendance" : data["attendance"] if "attendance" in data else 0,
                    "home_team": data["homeTeam"]["name"],
                    "away_team": data["awayTeam"]["name"],
                    "home_coach": data["homeTeam"]["coach"]["name"] if data["homeTeam"]["coach"] else "Unknown",
                    "away_coach": data["awayTeam"]["coach"]["name"] if data["awayTeam"]["coach"] else "Unknown",
                    "home_formation": data["homeTeam"]["formation"] if "formation" in data["homeTeam"] else "Unknown",
                    "away_formation": data["awayTeam"]["formation"] if "formation" in data["awayTeam"] else "Unknown",
                    "home_lineup": ', '.join(map(str, home_lineup_ids)),
                    "away_lineup": ', '.join(map(str, away_lineup_ids)),
                    "home_possession": data["homeTeam"]["statistics"]["ball_possession"] if "statistics" in data["homeTeam"] else 0,
                    "away_possession": data["awayTeam"]["statistics"]["ball_possession"] if "statistics" in data["awayTeam"] else 0,
                    "home_shots": data["homeTeam"]["statistics"]["shots"] if "statistics" in data["homeTeam"] else 0,
                    "away_shots": data["awayTeam"]["statistics"]["shots"] if "statistics" in data["awayTeam"] else 0,
                    "home_shots_on_goal": data["homeTeam"]["statistics"]["shots_on_goal"] if "statistics" in data["homeTeam"] else 0,
                    "away_shots_on_goal": data["awayTeam"]["statistics"]["shots_on_goal"] if "statistics" in data["awayTeam"] else 0,
                    "home_shots_off_goal": data["homeTeam"]["statistics"]["shots_off_goal"] if "statistics" in data["homeTeam"] else 0, 
                    "away_shots_off_goal": data["awayTeam"]["statistics"]["shots_off_goal"] if "statistics" in data["awayTeam"] else 0,
                    "home_free_kicks": data["homeTeam"]["statistics"]["free_kicks"] if "statistics" in data["homeTeam"] else 0,
                    "away_free_kicks": data["awayTeam"]["statistics"]["free_kicks"] if "statistics" in data["awayTeam"] else 0, 
                    "home_goal_kicks": data["homeTeam"]["statistics"]["goal_kicks"] if "statistics" in data["homeTeam"] else 0, 
                    "away_goal_kicks": data["awayTeam"]["statistics"]["goal_kicks"] if "statistics" in data["awayTeam"] else 0,
                    "home_offsides": data["homeTeam"]["statistics"]["offsides"] if "statistics" in data["homeTeam"] else 0, 
                    "away_offsides": data["awayTeam"]["statistics"]["offsides"] if "statistics" in data["awayTeam"] else 0, 
                    "home_saves": data["homeTeam"]["statistics"]["saves"] if "statistics" in data["homeTeam"] else 0, 
                    "away_saves": data["awayTeam"]["statistics"]["saves"] if "statistics" in data["awayTeam"] else 0, 
                    "home_throw_ins": data["homeTeam"]["statistics"]["throw_ins"] if "statistics" in data["homeTeam"] else 0, 
                    "away_throw_ins": data["awayTeam"]["statistics"]["throw_ins"] if "statistics" in data["awayTeam"] else 0,
                    "home_fouls": data["homeTeam"]["statistics"]["fouls"] if "statistics" in data["homeTeam"] else 0,
                    "away_fouls": data["awayTeam"]["statistics"]["fouls"] if "statistics" in data["awayTeam"] else 0,
                    "home_yellow_cards": data["homeTeam"]["statistics"]["yellow_cards"] if "statistics" in data["homeTeam"] else 0,
                    "away_yellow_cards": data["awayTeam"]["statistics"]["yellow_cards"] if "statistics" in data["awayTeam"] else 0,
                    "home_yellow_red_cards": data["homeTeam"]["statistics"]["yellow_red_cards"] if "statistics" in data["homeTeam"] else 0,
                    "away_yellow_red_cards": data["awayTeam"]["statistics"]["yellow_red_cards"] if "statistics" in data["awayTeam"] else 0,
                    "home_red_cards": data["homeTeam"]["statistics"]["red_cards"] if "statistics" in data["homeTeam"] else 0,
                    "away_red_cards": data["awayTeam"]["statistics"]["red_cards"] if "statistics" in data["awayTeam"] else 0,
                    "full_time_home": data["score"]["fullTime"]["home"] if "fullTime" in data["score"] else 0,
                    "full_time_away": data["score"]["fullTime"]["away"] if "fullTime" in data["score"] else 0,
                    "half_time_home": data["score"]["halfTime"]["home"] if "halfTime" in data["score"] else 0,
                    "half_time_away": data["score"]["halfTime"]["away"] if "halfTime" in data["score"] else 0
                }

                writer.writerow(match_info)
                print(f"Uloženo: {match_info['home_team']} vs {match_info['away_team']}")

                time.sleep(2)

            except KeyError as e:
                print(f"Chyba v zápasu {match_id}: {e}")

    print("Done")