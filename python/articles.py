#! /usr/bin/env python3
"""Script to obtain tidy article database from RePEc archives"""

import os
import pandas as pd


ROOT = "/home/rdora/rdf/per/pers"
SAVE = "/home/rdora/femec/data/"
pattern1 = "Handle"
pattern2 = "Short-Id"
pattern3 = "author-"

patterns = [pattern1,
            pattern2,
            pattern3]


data = []
for root, dirs, files in os.walk(ROOT):
    print(root)
    for personal_file in files:
        articles = []
        personal_file = os.path.join(root, personal_file)
        with open(personal_file, "r") as f:
            personal_list = f.read().splitlines()
        for line in personal_list:
            if line.startswith(pattern1):
                handle = line.split(":", 1)[1].strip()
            elif line.startswith(pattern2):
                short_id = line.split(":", 1)[1].strip()
            elif line.startswith(pattern3):
                item_type, item_id = line.split(":", 1)
                item_id = item_id.strip()
                item_type = item_type.split("-")[1]
                articles.append([item_type, item_id])
        rows = [[handle, short_id, x, y] for x, y in articles]
        data.extend(rows)

df = pd.DataFrame(
    data, columns=["Author-Handle", "Short-Id", "Item-Type", "Item-Id"])
df.to_csv(os.path.join(SAVE, "article.csv"), index=False)
