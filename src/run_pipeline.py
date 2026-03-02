import numpy as np
import pandas as pd
#from data_cleaning import cfb_results_merger as crm
#from scraping import performance_scraper as ps
#from scraping import rankings_scraper as rs

from data_cleaning.cfb_results_merger import (
    build_game_stats,
    build_season_stats,
    calculate_sos,
    save_outputs
)

if __name__ == "__main__":
    years = range(2015, 2026)
    games = build_game_stats(years)
    print("games built")
    season_stats = build_season_stats(games)
    print("season_stats built")
    sos = calculate_sos(games, season_stats)
    print("sos calculated")
    save_outputs(season_stats, sos)