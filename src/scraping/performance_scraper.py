import pandas as pd
import requests
from datetime import datetime, timedelta
import json
import time

def fetch_season(year):
    start = datetime(year, 8, 1)
    end = datetime(year+1, 1, 31)
    
    all_games = []
    current = start
    
    while current <= end:
        time.sleep(0.1)
        date_str = current.strftime("%Y%m%d")
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={date_str}"
        
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            all_games.extend(data.get("events", []))
        
        current += timedelta(days=1)
    print(all_games)
    unique_games = {game["id"]: game for game in all_games}
    
    return list(unique_games.values())

def load_games(years):
    for year in years:
        print(f"Fetching games for year: {year}")
        games = fetch_season(year)
        with open(f"../../data/raw/cfb_games_{year}.json", "w") as f:
            json.dump(games, f)
        
#    full_df = pd.concat(dfs, ignore_index=True)
#    full_df.to_csv("../../data/raw/cfb_games.csv", index=True)

if __name__ == "__main__":
    years = range(2019, 2026)
    load_games(years)
    