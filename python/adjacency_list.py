#!/usr/bin/env python3
"""Script to translate paper-based to author-based citations adjacency list"""

import collections
import itertools
import pandas as pd

p2al = "/home/rdora/femec/data/iscited.txt"
articles = "/home/rdora/femec/data/processed/article.csv"
output = "/home/rdora/femec/data/processed/cites.csv"

article = pd.read_csv(articles)
# Only article items
print("Number of authors:", article['Short-Id'].nunique())
print("Number of articles:", article['handle'].nunique())
dict_article = collections.defaultdict(dict)
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

header = ['target', 't_year', 't_journal', 'source', 's_year', 's_journal']
with open(p2al) as f:
    for line in f:
        # u, v nodes where u is the main node
        try:
            u, v = line.split()
        except ValueError:
            print(line)
            raise ValueError
        u = u.lower()
        if u in dict_article:
            authors = dict_article[u]['authors']
            year = dict_article[u]['year']
            journal = dict_article[u]['journal']
            refs = v.split("#")
            for ref in refs:
                ref = ref.lower()
                if ref in dict_article:
                    ref_authors = dict_article[ref]['authors']
                    ref_year = dict_article[ref]['year']
                    ref_journal = dict_article[ref]['journal']
                    for u, v in itertools.product(authors, ref_authors):
                        data.append([u,
                                     year,
                                     journal,
                                     v,
                                     ref_year,
                                     ref_journal])

pd.DataFrame(data, columns=header).to_csv(output, index=False)
