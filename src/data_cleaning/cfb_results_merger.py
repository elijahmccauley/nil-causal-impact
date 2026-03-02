import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import ast
from scraping import performance_scraper as ps
import json

conference_mapping = {
    "ACC": 1,
    "BIG 12": 4,
    "BIG 10": 5,
    "SEC": 8,
    "PAC-12": 9,
    "MAC": 15,
    "Mountain West": 17,
    "Sun Belt": 37,
    "American (AAC)": 151,
}
fbs_conferences = {"8","5","1","4","9","151","17","15","37"}

def build_game_stats(years):
    all_rows = []
    for year in years:
        print(f"Processing year: {year}")
        with open(f"../data/raw/cfb_games_{year}.json") as f:
            games = json.load(f)
        
        for game in games:
            competitions = game["competitions"]
            status = game["status"]
            
            if not status["type"]["completed"]:
                continue
            
            competitors = competitions[0]["competitors"]
            home = next(c for c in competitors if c["homeAway"] == "home")
            away = next(c for c in competitors if c["homeAway"] == "away")
            home_team = home["team"]["displayName"]
            away_team = away["team"]["displayName"]

            home_score = int(home["score"])
            away_score = int(away["score"])
            
            margin = abs(home_score - away_score)
            close_game = margin <= 7

            home_conf = home["team"].get("conferenceId")
            away_conf = away["team"].get("conferenceId")
            conf_game = home_conf is not None and away_conf is not None and home_conf == away_conf
            if str(home_conf) not in fbs_conferences:
                continue
            if str(away_conf) not in fbs_conferences:
                continue
            all_rows.append({
                "team": home_team,
                "opponent": away_team,
                "year": year,
                "points_for": home_score,
                "points_against": away_score,
                "win": int(home_score > away_score),
                "conference": home_conf,
                "conf_game": conf_game,
                "conf_win": int(home_score > away_score) if conf_game else None,
                "close_game": close_game,
                "close_win": int(home_score > away_score) if close_game else None
            })
            
            all_rows.append({
                "team": away_team,
                "opponent": home_team,
                "year": year,
                "points_for": away_score,
                "points_against": home_score,
                "win": int(away_score > home_score),
                "conference": away_conf,
                "conf_game": conf_game,
                "conf_win": int(away_score > home_score) if conf_game else None,
                "close_game": close_game,
                "close_win": int(away_score > home_score) if close_game else None
            })
            
            
    all_rows_df = pd.DataFrame(all_rows)
    return all_rows_df

def build_season_stats(df):
    season_stats = (
        df.groupby(["team", "year", "conference"])
            .agg(
                wins=("win", "sum"),
                games=("win", "count"),
            points_for=("points_for", "sum"),
            points_against=("points_against", "sum"),
            conf_wins=("conf_win", "sum"),
            conf_games=("conf_game", "sum"),
            close_wins=("close_win", "sum"),
            close_games=("close_game", "sum"),
        )
    .reset_index()
    )

    season_stats["losses"] = season_stats["games"] - season_stats["wins"]
    season_stats["win_pct"] = season_stats["wins"] / season_stats["games"]
    season_stats["avg_point_diff"] = (
        (season_stats["points_for"] - season_stats["points_against"]) 
        / season_stats["games"]
    )
    season_stats["conf_win_pct"] = (
        season_stats["conf_wins"] 
        / season_stats["conf_games"]
    ).fillna(0)

    season_stats["close_win_pct"] = (
        season_stats["close_wins"] 
        / season_stats["close_games"]
    ).fillna(0)

    season_stats["point_diff_total"] = (
        season_stats["points_for"] 
        - season_stats["points_against"]
    )

    return season_stats

def calculate_sos(df, season_stats):
    opp_win = season_stats[["team", "year", "win_pct"]].rename(
        columns={"team": "opponent", "win_pct": "opp_win_pct"}
    )

    sos_df = df.merge(
        opp_win,
        on=["opponent", "year"],
        how="left"
    )

    sos = (
        sos_df.groupby(["team", "year", "conference"])
        .agg(sos=("opp_win_pct", "mean"))
        .reset_index()
    )
    return sos

def save_outputs(season_stats, sos):
    season_stats = season_stats.merge(sos, on=["team", "year", "conference"], how="left")


    season_stats.to_csv("../data/processed/cfb_season_stats.csv", index=False)


if __name__ == "__main__":
    games = build_game_stats(years=range(2015, 2026))
    season_stats = build_season_stats(games)
    sos = calculate_sos(games, season_stats)
    save_outputs(season_stats, sos)


#### NEXT STEPS: MODULARIZE INTO FUNCTIONS, MAKE SURE CONFERENCE IS SAVED THROUGHOUT (PREVENT FCS) DONT WANT TO JUST REMOVE NECESSARILY BUT THEIR WIN PCT IS COOKED SO MIGHT BE NECESSARY, IMPROVE SOS CALCULATION