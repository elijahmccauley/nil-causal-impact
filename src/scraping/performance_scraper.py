import pandas as pd
import requests
from datetime import datetime, timedelta

def fetch_season(year):
    all_games = []
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={year}"
        
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        for event in data.get("events", []):
            all_games.append(event)
    
    return all_games

def load_games(years):
    all_games = []
    for year in years:
        games = fetch_season(year)
        print(f"Year {year}: {len(games)} games")
        all_games.extend(games)
        
    df = pd.DataFrame(all_games)
    df.to_csv("../../data/raw/cfb_games.csv", index=True)
    