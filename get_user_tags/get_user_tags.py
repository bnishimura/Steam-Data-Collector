'''
this is run after filter_by_tag.py
takes entries on a csv, goes to its store page like
https://store.steampowered.com/app/1145360
and scrapes the user defined tags with regex

examples of particular tags:
3D - re has to find numbers and letters
Free to Play - re has to get spaces
Sci-fi - re has to match dash
2.5D - match dot
LGBTQ+ - match plus
in steam, user tags are surrounded by space characters like \n, \t

writes a wide table? appid | is_action | is_mmo ... ?
or a two column table? appid | tag_list ?
or a non starndard table (each row has different lengths)
or we dump straight into a database

preferred: build a csv 'non standard' table so we save progress reliably
(it involves requests and it might take a day or two at a rate of one 
request per second) and then we put the csv into a database
'''
import requests
import re
import csv
import time
import datetime


def save_batch(rows, i):
    with open('idx_tag.csv', 'w') as tag_tbl:
        writer = csv.writer(tag_tbl, lineterminator='\n')
        for row in rows:
            writer.writerow(row)

    with open('tag_batch_info.txt', 'w') as batch:
        batch.write('{}'.format(i+1))

    print('Progress has been saved')

with open('idx_tag.csv', 'r') as apps:
    reader = csv.reader(apps)
    rows = []
    for row in reader:
        rows.append(row)

with open('tag_batch_info.txt', 'r') as batch:
    curr_idx = batch.readline()
    # if batch tracker file if empty, give 0 to curr_idx
    curr_idx = 0 if not curr_idx else int(curr_idx)

PATH = 'https://store.steampowered.com/app/'
# PATTERN = '<a.*class="app_tag".*>\s*([\w\- \.\+]+)\s*</a>+?'
PATTERN = '<a.*class="app_tag".*>\s*([\S ]+)\s*</a>+?'
TIME_LIMIT = datetime.time(23, 25)
now = datetime.datetime.now().time()

count = 0
batch_idx = curr_idx
for i in range(curr_idx, len(rows)):
    if now > TIME_LIMIT: break
    game_id = rows[i][0]
    print(game_id)
    response = requests.get(PATH + game_id)
    data = response.text
    tags = re.findall(PATTERN, data)
    rows[i].extend(tags)

    count += 1
    batch_idx = i
    if count >= 50:
        save_batch(rows, i)
        count = 0
    now = datetime.datetime.now().time()

    print('\n')
    time.sleep(1)

save_batch(rows, batch_idx)
