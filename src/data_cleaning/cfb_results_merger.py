import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import ast

all_rows = []
for year in range(2015, 2026):
    games_df = pd.read_csv(f"../../data/raw/cfb_games_{year}.csv")
    
    for _, row in games_df.iterrows():
        competitions = ast.literal_eval(row["competitions"])
        status = ast.literal_eval(row["status"])
        
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

season_stats = (
    all_rows_df.groupby(["team", "year"])
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

opp_win = season_stats[["team", "year", "win_pct"]].rename(
    columns={"team": "opponent", "win_pct": "opp_win_pct"}
)

sos_df = all_rows_df.merge(
    opp_win,
    on=["opponent", "year"],
    how="left"
)
print(sos_df["opp_win_pct"].isna().sum())

sos = (
    sos_df.groupby(["team", "year"])
      .agg(sos=("opp_win_pct", "mean"))
      .reset_index()
)
season_stats = season_stats.merge(sos, on=["team", "year"], how="left")


season_stats.to_csv("../../data/processed/cfb_season_stats.csv", index=False)




#### NEXT STEPS: MODULARIZE INTO FUNCTIONS, MAKE SURE CONFERENCE IS SAVED THROUGHOUT (PREVENT FCS) DONT WANT TO JUST REMOVE NECESSARILY BUT THEIR WIN PCT IS COOKED SO MIGHT BE NECESSARY, IMPROVE SOS CALCULATION