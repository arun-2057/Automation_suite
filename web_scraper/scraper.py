import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime


def fetch_page(url):
    """Fetch page content safely."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_headlines(html):
    """Extract news headlines from Hacker News."""
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.select(".titleline > a")   # HN's headline selector

    headlines = []
    for t in titles:
        headlines.append({
            "title": t.get_text(strip=True),
            "url": t["href"]
        })

    return headlines


def save_json(data, filename="headlines.json"):
    """Save headlines to JSON."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved JSON → {filename}")


def save_csv(data, filename="headlines.csv"):
    """Save headlines to CSV."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "URL"])
        for item in data:
            writer.writerow([item["title"], item["url"]])
    print(f"Saved CSV → {filename}")


def main():
    url = "https://news.ycombinator.com/"
    print("Fetching latest headlines...")

    html = fetch_page(url)
    headlines = parse_headlines(html)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    json_file = f"headlines_{timestamp}.json"
    csv_file = f"headlines_{timestamp}.csv"

    save_json(headlines, json_file)
    save_csv(headlines, csv_file)

    print(f"Scraped {len(headlines)} headlines successfully!")


if __name__ == "__main__":
    main()
