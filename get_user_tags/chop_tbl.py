'''
takes a csv table and cuts some columns out
we need 'appid' to identify the game
and 'type' to know whether it is a game or not
'''
import csv


with open('../fetch_apps/app_list.csv', 'r') as apps:
    reader = csv.reader(apps)
    rows = []
    for row in reader:
        rows.append(row)

idx_column = rows[0].index('appid')
type_column = rows[0].index('type')
max_idx = max(idx_column, type_column)

with open('idx_tag.csv', 'w') as chopped:
    writer = csv.writer(chopped, lineterminator='\n')
    for row in rows:
        if len(row) < max_idx+1:
            row = row + ['UNKNOWN']*(max_idx+1 - len(row))
        if row[type_column] == 'game':
            writer.writerow(row[idx_column])
