#!/usr/bin/env python3
"""Get journal information"""
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
    re_temp = re.compile('ReDIF-Series', flags=re.IGNORECASE)
    re_handle = re.compile('handle', flags=re.IGNORECASE)
    re_type = re.compile('type', flags=re.IGNORECASE)
    re_name = re.compile('name', flags=re.IGNORECASE)
    data = []
    inside = False
    for n, line in enumerate(line_list):
        if re_temp.search(line):
            if inside:
                data.append(three)
            # First time encounterd this template
            inside = True
            three = ['', '', '']
        if inside:
            if re_name.match(line):
                # Always one colon separating key and value
                name = line.split(':')[1].strip().replace('"', "'")
                name = f'"{name}"'
                three[1] = name
                if n == (len(line_list) - 1):
                    data.append(three)
                    inside = False
            elif re_type.match(line):
                jtype = line.split(':')[1].strip()
                three[2] = jtype
                if n == (len(line_list) - 1):
                    data.append(three)
                    inside = False
            elif re_handle.match(line):
                handle = line.split(':', 1)[1].strip()
                three[0] = handle
                if n == (len(line_list) - 1):
                    data.append(three)
                    inside = False
            elif n == (len(line_list) - 1):
                data.append(three)
                inside = False
    if not data:
        print(line_list)

    return data


if __name__ == '__main__':
    """Obtain all journal data"""

    files_path = '/home/rdora/femec/data/journal_files.txt'
    output_file = '/home/rdora/femec/data/journals.csv'
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
    data.insert(0, ['handle', 'name', 'type'])
    with open(output_file, 'w') as f:
        for line in data:
            f.write(','.join(line))
            f.write('\n')
