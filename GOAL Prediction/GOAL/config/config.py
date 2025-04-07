import json

with open("config/config.json") as f:
    config = json.load(f)

key = config["key"]
url = config["url"]

