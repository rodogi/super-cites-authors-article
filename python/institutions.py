#! /usr/bin/env python3
"""Script to obtain institution database from RePEc archives"""

import os
import pandas as pd


ROOT = "/home/rdora/rdf/edi/inst"
SAVE = "/home/rdora/femec/data/"
pattern1 = "Handle"
pattern2 = "Primary-Name"
pattern3 = "Primary-Location"

patterns = [pattern1,
            pattern2,
            pattern3]


data = []
for root, dirs, files in os.walk(ROOT):
    print(root)
    for personal_file in files:
        personal_file = os.path.join(root, personal_file)
        row = ["" for _ in range(5)]
        with open(personal_file, "r") as f:
            personal_list = f.read().splitlines()
        for i, pattern in enumerate(patterns):
            for line in personal_list:
                if pattern in line:
                    entry = line.split(":", 1)[1].strip()
                    if pattern == pattern3 and (len(entry.split(",")) == 2):
                        print(line)
                        city, country, state = "", "", ""
                        city, country = entry.split(",")
                        # Country may conain spaces
                        country = country.strip()
                        if "(" in country:
                            state, country = country.split("(")
                            state = state.strip()
                            country = country[:-1]
                        row[2] = city
                        row[3] = state
                        row[4] = country
                    elif pattern == pattern3:
                        row[i] = entry
                    else:
                        row[i] = entry
        data.append(row)

df = pd.DataFrame(
    data, columns=[pattern1, pattern2, "city", "state", "country"])
df.to_csv(os.path.join(SAVE, "institution.csv"), index=False)
