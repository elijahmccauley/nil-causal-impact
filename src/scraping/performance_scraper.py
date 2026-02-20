import pandas as pd
import requests
from datetime import datetime, timedelta

all_games = []
def fetch_season(year):
    start = datetime(year, 8, 1)
    end = datetime(year+1, 1, 31)
    
    all_games = []
    current = start
    
    while current <= end:
        date_str = current.strftime("%Y%m%d")
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={year}"
        
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            for event in data.get("events", []):
                all_games.append(event)
        
        current += timedelta(days=1)
    
    return all_games

for year in range(2015, 2026):
    games = fetch_season(year)
    print(f"Year {year}: {len(games)} games")
    all_games.extend(games)
    
df = pd.DataFrame(all_games)
df.to_csv("../../data/raw/cfb_games.csv", index=True)
    