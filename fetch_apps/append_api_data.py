'''
This script will extend the csv created by parse_list.py by using data from
https://store.steampowered.com/api/appdetails/?appids=<appid>

The project only requires the "type" field of the request, so we can filter out
dlcs, tools, test entries and other stuff. For the sake of completeness, it also
fetches:
    whether or not the game is free
    categories
    genres
    price 
    supported languages
    release date

WE ARE LIMITED TO 100K REQUESTS PER DAY - AROUND 1.15 PER SECOND

also, I am aware some parts of this script is very poorly done (haha)
'''
import csv
import requests
import time
import datetime


def save_progress(rows, i):
    print('saving progress\n')
    with open('app_list.csv', 'w') as applist:
        writer = csv.writer(applist, lineterminator='\n')
        for line in rows:
            writer.writerow(line)

    with open('batch_info.txt', 'w') as batch_info:
        batch_info.write('{}'.format(i-1))

with open('app_list.csv', 'r') as applist:
    reader = csv.reader(applist)

    rows = []
    for row in reader:
        rows.append(row)
    if len(rows[0]) <= 2: # we might run this script multiple times
        rows[0].extend(['type', 'is_free', 'price (BRL)', \
                'categories', 'genres', 'release_date'])

BASE_URL = 'https://store.steampowered.com/api/appdetails/?json=1&appids='
with open('batch_info.txt') as batch_info:
    # batch_info holds data related to the state of the data fetching
    # int (last read line)
    # string (timestamp for the maximum time allowed for the script to run)
    prev_index = int(batch_info.readline())

TIME_LIMIT = datetime.time(23, 25)
now = datetime.datetime.now().time()
target = len(rows)

# need i to save in batch_info 
i = prev_index+1
count = 0
while i in range(prev_index+1, target) and now < TIME_LIMIT:
    # the time check exists because I like to turn off my pc when I go to sleep :)
    appid = rows[i][0]
    print(i)
    print(appid)
    response = requests.get(BASE_URL + appid)

    # null is returned when steam doesn't want to serve
    while response.text == 'null':  
        time.sleep(5)
        response = requests.get(BASE_URL + appid)
    # some responses come as
    # SyntaxError: JSON.parse: unexpected end of data at line 1 column 1 of the JSON data
    # in which case, text == b''
    # ideally we should check for raises from response.json() and deal with the problem
    # properly. We might not need to do it though
    if response.text:
        response = response.json()[appid]
    else: 
        i += 1
        count += 1
        continue
    # this causes blank lines on the data set
    is_success = response['success']
    # we have no guarantees about what fields are filled, hence the multiple checks
    # remember that text fields may have any utf-8 characters
    if is_success and 'data' in response:
        data = response['data']
        if 'type' in data:
            app_type = data['type']
        else: continue
        is_free = data['is_free']
        coming_soon = data['release_date']['coming_soon']
        if coming_soon:
            release_date = "NOT RELEASED"
            price = "NOT RELEASED"
        else:
            if 'release_date' in data:
                release_date = data['release_date']['date']
            else: release_date = 'UNKNOWN'
            if 'price_overview' in data:
                price = 'R$ 0,00' if is_free else data['price_overview']['final_formatted']
            else: 
                price = 'R$ 0,00' if is_free else 'UNKNOWN'
#        if 'detailed_description' in data:
#            description = data['detailed_description'].encode('ascii', 'ignore').decode('utf-8')
#        else: description = ''
        if 'categories' in data:
            categories = data['categories']
        else: categories = []
        if 'genres' in data:
            genres = data['genres']
        else: genres = []

        rows[i].extend([app_type, is_free, price, categories, genres, release_date])
        print(rows[i])
    print('\n')
    now = datetime.datetime.now().time()
    i += 1
    count += 1
    if count >= 50:
        save_progress(rows, i)
        count = 0
    time.sleep(1)

save_progress(rows, i)

# TO DO
# receiving null responses - MUST WAIT and decrease requests

