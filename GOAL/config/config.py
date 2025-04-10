import json

with open("config/config.json") as f:
    config = json.load(f)

key = config["key"]
base_url = config["base_url"]
headers = {"X-Auth-Token": key}
ai_model = config["model"]

