#! /usr/bin/env python3
"""Script to obtain author database from RePEc archives"""

import os
import pandas as pd


ROOT = "/home/rdora/rdf/per/pers"
SAVE = "/home/rdora/femec/data/"
pattern1 = "Handle"
pattern2 = "Short-Id"
pattern3 = "Workplace-Institution"
pattern4 = "Name-First"
pattern5 = "Name-Middle"
pattern6 = "Name-Last"
pattern7 = "Name-Full"
pattern8 = "Registered-Date"
pattern9 = "Last-Login-Date"

patterns = [pattern1,
            pattern2,
            pattern3,
            pattern4,
            pattern5,
            pattern6,
            pattern7,
            pattern8,
            pattern9]


data = []
for root, dirs, files in os.walk(ROOT):
    print(root)
    for personal_file in files:
        personal_file = os.path.join(root, personal_file)
        row = ["" for _ in range(len(patterns))]
        with open(personal_file, "r") as f:
            personal_list = f.read().splitlines()
        for i, pattern in enumerate(patterns):
            for line in personal_list:
                if pattern in line:
                    entry = line.split(":", 1)[1].strip()
                    row[i] = entry
        data.append(row)

df = pd.DataFrame(data, columns=patterns)
df.to_csv(os.path.join(SAVE, "author.csv"), index=False)
