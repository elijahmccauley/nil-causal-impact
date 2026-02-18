import pandas as pd
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    all_data = []
    for year in range(2015, 2026):
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://247sports.com/season/{year}-football/compositeteamrankings/")
        
        # Click “Load More” until it disappears
        while page.locator("a[data-js='showmore']").is_visible():
            page.locator("a[data-js='showmore']").click()
            page.wait_for_timeout(1000)

        content = page.content()
        soup = BeautifulSoup(content, "html.parser")
        rows = soup.select("li.rankings-page__list-item")

        data = []
        for row in rows:
            rank = row.select_one(".rank-column").text.strip()
            
            rank = rank.split()
            primary_rank = rank[0]
            other_rank = rank[1]
            try:
                team = row.select_one(".team a").text.strip()
            except AttributeError:
                team = row.select_one(".team").text.strip()
            try:
                total = row.select_one(".total a").text.strip()
            except AttributeError:
                total = row.select_one(".total").text.strip()
            avg = row.select_one(".avg").text.strip()
            try:
                points = row.select_one(".points a").text.strip()
            except AttributeError:
                points = row.select_one(".points").text.strip()
            
            data.append({"team": team, "year": year, "primary_rank": primary_rank, "other_rank": other_rank, "total": total, "avg": avg, "points": points})
        all_data.extend(data)
    browser.close()
df = pd.DataFrame(all_data)
df.to_csv("../../data/raw/recruiting_rankings.csv", index=True)