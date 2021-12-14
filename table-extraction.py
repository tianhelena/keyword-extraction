#!/usr/bin/env python

import pylightxl as xl
import json
import string

def build_json(current_keys, row):
    if row.is_empty():
        return ""


# set the delimiter of the CSV to be the value of your choosing
# set the default worksheet to write the read in CSV data to
db = xl.readxl(fn='/Users/wenshuaihou/code/keyword-extraction/GEO.xlsx')
ws = db.ws("Table 1")

clean_rows = []
for i, row in enumerate(ws.rows):

    if i == 0:
        clean_rows.append(row)
    else:
        first_non_empty = next(i for i,cell in enumerate(row) if cell.strip())
        clean_row = clean_rows[-1][:first_non_empty] + row[first_non_empty:]
        clean_rows.append(clean_row)

data = {}
for row in clean_rows:
    current_level = data
    for cell in row:
        cell = ''.join(filter(lambda c: c in string.printable, cell)).strip()
        if cell not in current_level:
            current_level[cell] = {}
        current_level = current_level[cell]
with open('./table.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# data_list = []

# for rownum in range(1, sh.nrows):
#     data = OrderedDict()

# row_values = sh.row_values(rownum)
# data['<Column Name1>'] = row_values[0]
# data['<Column Name2>'] = row_values[1]
# data_list.append(data)
