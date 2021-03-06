#!/usr/bin/env python

import pylightxl as xl
import json
import string

def build_json(rows):
    d = {}
    for path in rows:
        current_level = d
        for part in path:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
    return d

def is_header(row):
    return row[0].strip() and all([not cell.strip() for cell in row[1:]])
# set the delimiter of the CSV to be the value of your choosing
# set the default worksheet to write the read in CSV data to
db = xl.readxl(fn='./GEO.xlsx')
ws = db.ws("Table 1")

clean_rows = []
for i, row in enumerate(ws.rows):

    if i == 0:
        clean_rows.append(row)
    else:
        first_non_empty = next(i for i,cell in enumerate(row) if cell.strip())
        clean_row = clean_rows[-1][:first_non_empty] + row[first_non_empty:]
        clean_row = [ ''.join(filter(lambda c: c in string.printable, cell)).strip() for cell in clean_row]
        clean_rows.append(clean_row)

datas = []
section = []
for row in clean_rows:
    if not section:
        section.append(row)
    elif is_header(row):
        datas.append({section[0][0] : build_json(section[1:])})
        section = [row]
    else:
        section.append(row)

with open('./table.json', 'w', encoding='utf-8') as f:
    json.dump(datas, f, ensure_ascii=False, indent=4)

