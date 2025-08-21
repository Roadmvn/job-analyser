#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup


def test_scraping(url: str):
    r = requests.get(url, timeout=20)
    print(f"GET {url} -> {r.status_code}")
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = [t.get_text(strip=True) for t in soup.find_all('h1')]
    for t in titles[:10]:
        print(f"h1: {t}")


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://example.com'
    test_scraping(url)


