#! /usr/bin/env python3
"""Script to obtain the RePEc id of top 10% female economists."""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path


URL = "https://ideas.repec.org/top/top.women.html"
SAVE = "/home/rdora/femec/data/top_femec.csv"
resp = requests.get(URL)
soup = BeautifulSoup(resp.text, 'html.parser')

people_href = []
for a in soup.find_all('a', href=True):
    if a['href'].startswith("/e/") or a['href'].startswith("/f/"):
        short_id = Path(a['href']).stem
        people_href.append([short_id, 'F'])

df = pd.DataFrame(people_href, columns=["short_id", "gender"])
df.to_csv(SAVE, index=False)
