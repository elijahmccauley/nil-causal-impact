import pandas as pd
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://247sports.com/season/2025-football/compositeteamrankings/")
    
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
        print(rank)
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
        
        print(team)
        data.append({"rank": rank, "team": team, "total": total, "avg": avg, "points": points})

    browser.close()
df = pd.DataFrame(data)
df.to_csv("2025_recruiting.csv", index=False)


'''with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://247sports.com/season/2025-football/compositeteamrankings/")
    
    while page.locator("a[data-js='showmore']").is_visible():
        page.locator("a[data-js='showmore']").click()
        page.wait_for_timeout(1500)
    
    content = page.content()
    print(content[:500])  # Print the first 500 characters to verify content
    browser.close()
    
all_rows = []
year = 2025
soup = BeautifulSoup(content, "html.parser")
        
rows = soup.select(".wrapper")  # adjust selector after inspection
        
if not rows:
    print("Rows not found, stopping.")
        
for row in rows:
    rank = row.select_one(".rank-column").text.strip()
    team = row.select_one(".team-name").text.strip()
    total = row.select_one(".total").text.strip()
    avg = row.select_one(".avg").text.strip()
    points = row.select_one(".points").text.strip()
    
    all_rows.append({
        "year": year,
        "rank": rank,
        "team": team,
        "total": total,
        "avg": avg,
        "points": points
    })
        
    
df = pd.DataFrame(all_rows)

df.to_csv("2025_recruiting.csv", index=False)



'''





'''BASE_URL = "https://247sports.com/season/{year}-football/compositeteamrankings/"
session = requests.Session()

def fetch_recruiting(year):
    all_rows = []
    page = 1
    
    while True:
        url = f"{BASE_URL.format(year=year)}?Page={page}"
        print(url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Referer": "https://247sports.com/",
        }
        base_url = "https://247sports.com/season/2025-football/compositeteamrankings/"
        session.get(base_url, headers=headers)
        url = base_url + "?Page=2"
        response = session.get(url, headers=headers)

        print(response.status_code)
        print(response.text[:500])
        
        if response.status_code != 200:
            print(f"Failed to fetch page {page} for year {year}. Status code: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        rows = soup.select(".wrapper")  # adjust selector after inspection
        
        if not rows:
            print("Rows not found, stopping.")
            break
        
        for row in rows:
            rank = row.select_one(".rank-column").text.strip()
            team = row.select_one(".team-name").text.strip()
            total = row.select_one(".total").text.strip()
            avg = row.select_one(".avg").text.strip()
            points = row.select_one(".points").text.strip()
            
            all_rows.append({
                "year": year,
                "rank": rank,
                "team": team,
                "total": total,
                "avg": avg,
                "points": points
            })
        
        page += 1
    
    return pd.DataFrame(all_rows)

df = fetch_recruiting(2025)
df.to_csv("2025_recruiting.csv", index=False)'''