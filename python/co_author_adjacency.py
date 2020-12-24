#!/usr/bin/env python3
"""Script to translate paper-based to author-based co-author adjacency list"""

import collections
import itertools
import pandas as pd
import numpy as np

articles = "/home/rdora/femec/data/processed/article.csv"
output = "/home/rdora/femec/data/processed/co_author.csv"

article = pd.read_csv(articles)
# Only article items
print("Number of authors:", article['Short-Id'].nunique())
print("Number of articles:", article['handle'].nunique())
header = ['author1', 'author2', 'article',
          'year', 'journal', 'journal_name', 'title']
dict_article = collections.defaultdict(dict)
dict_co_author = dict()
data = []

# Fill dict with article information
for i, row in article.iterrows():
    paper = row['handle']
    author = row['Short-Id']
    year = row['year']
    journal_id = row['journal']
    journal_name = row['name']
    title = row['title']
    dict_article[paper].setdefault('authors', [])
    dict_article[paper]['authors'].append(author)
    dict_article[paper].setdefault('year', str(year))
    dict_article[paper].setdefault('journal', journal_id)
    dict_article[paper].setdefault('journal_name', str(journal_name))
    dict_article[paper].setdefault('title', str(title))

for article in dict_article:
    paper = dict_article[article]
    for v, u in itertools.combinations(paper['authors'], 2):
        data.append([u, v, article, paper['year'],
                     paper['journal'],
                     paper['journal_name'],
                     paper['title']])
# Remove duplicates, the graph is non-directed
pd.DataFrame(data, columns=header).to_csv(output, index=False)
