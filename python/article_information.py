#!/usr/bin/env python3
"""Look for additional information of each article

Specificaly, look for the date, journal and title of the article.
"""
import re


def template_data(line_list):
    """Return the positions spanning each template type

    Arguments
    ---------
    line_list: list, list containing the repec file lines.

    Returns
    -------
    data: list, list of 3-list data included in each journal chunk.
    """
    re_temp = re.compile('ReDIF-Article', flags=re.IGNORECASE)
    re_handle = re.compile('handle:', flags=re.IGNORECASE)
    re_title = re.compile('title:', flags=re.IGNORECASE)
    re_year = re.compile('year:', flags=re.IGNORECASE)
    re_month = re.compile('month:', flags=re.IGNORECASE)
    re_journal = re.compile('journal:', flags=re.IGNORECASE)
    data = []
    inside = False
    for n, line in enumerate(line_list):
        if re_temp.search(line):
            if inside:
                data.append(five)
            inside = True
            five = ['', '', '', '', '', '']
        if inside:
            if re_title.match(line):
                # Always one colon separating key and value
                title = line.split(':')[1].strip().replace('"', "'")
                title = f'"{title}"'
                five[1] = title
                if n == (len(line_list) - 1):
                    data.append(five)
                    inside = False
            elif re_year.match(line):
                year = line.split(':')[1].strip()
                year = f'"{year}"'
                five[2] = year
                if n == (len(line_list) - 1):
                    data.append(five)
                    inside = False
            elif re_month.match(line):
                month = line.split(':')[1].strip()
                month = f'"{month}"'
                five[3] = month
                if n == (len(line_list) - 1):
                    data.append(five)
                    inside = False
            elif re_journal.match(line):
                journal = line.split(':')[1].strip().replace('"', "'")
                journal = f'"{journal}"'
                five[5] = journal
                if n == (len(line_list) - 1):
                    data.append(five)
                    inside = False
            elif re_handle.match(line):
                handle = line.split(':', 1)[1].strip()
                jhandle = handle.rsplit(':', 8)[0].strip()
                handle = f'"{handle}"'
                five[0] = handle
                five[4] = jhandle
                if n == (len(line_list) - 1):
                    data.append(five)
                    inside = False
            elif n == (len(line_list) - 1):
                data.append(five)
                inside = False

    return data


if __name__ == '__main__':
    """Obtain all journal data"""

    files_path = '/home/rdora/femec/data/article_files.txt'
    output_file = '/home/rdora/femec/data/articles_supp.csv'
    data = []
    with open(files_path) as f:
        files = f.read().splitlines()
    for journal_file in files:
        try:
            with open(journal_file, encoding='utf-8') as f:
                journal = f.read().splitlines()
        except UnicodeDecodeError:
            with open(journal_file, encoding='latin') as f:
                journal = f.read().splitlines()
        data.extend(template_data(journal))
    data.insert(0, ['handle', 'title', 'year', 'month', 'jhandle', 'jname'])
    with open(output_file, 'w') as f:
        for line in data:
            f.write(','.join(line))
            f.write('\n')
