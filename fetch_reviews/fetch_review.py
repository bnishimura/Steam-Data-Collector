# might reuse this module for multiple game fetches
import requests
import os
import pandas as pd
import json
import time
import csv
import datetime
from urllib.parse import quote_plus
from pathlib import Path


CWD = os.getcwd()
TIME_LIMIT = datetime.time(23, 25)
time_over = False

def build_query(cursor):
    cursor = quote_plus(cursor)
    query = '?json=1&language=english&filter=recent&cursor={}&purchase_type=all&num_per_page=100'.format(cursor)
    return query

def make_request(url):
    response = requests.get(url)
    while response.text == 'null' or 500 < response.status_code < 550:
        print('stalling\n')
        time.sleep(5)
        response = requests.get(url)

    if response.text:
        response = response.json()
    else:
        response = {'reviews' : ''}
    return response

def save_csv(df, path):
    print("saving csv")
    if not df.empty:
        if os.path.isfile(path):
            df.to_csv(path, mode='a', header=False, index=False)
        else:
            df.to_csv(path, mode='w' , index=False)

def fetch_review(game_id):
    '''
    must receive game_id so we can make the request
    also need game name so we can save a csv file for the game

    returns nothing, but dumps a csv file per game
    '''
    # might not use csv_name instead, we might use game_id
    # csv_name = '_'.join(game_name.lower().split(' ')) + ".csv"
    csv_path = Path(CWD + '/game_reviews/' + game_id + '.csv')
    review_url = 'http://store.steampowered.com/appreviews/{}'.format(game_id)
    cursor = "*"
    query = build_query(cursor)

    # response = requests.get(review_url + query).json()
    response = make_request(review_url + query)
    df_reviews = pd.DataFrame([])
    # must check for hiccups like when the api returns null
    print('getting reviews')
    while response['reviews']:
        print("gid, c, ct: ", game_id, cursor, '\n')
        reviews = response['reviews']  # 100 or less reviews
        batch_df = pd.DataFrame.from_dict(reviews)  # batch of reviews
        df_reviews = pd.concat([df_reviews, batch_df])
        # this is bad. if the loop breaks we end up with a half filled csv
        # and no way to add from where we stopped

        now = datetime.datetime.now().time()
        cursor = response['cursor']
        if now > TIME_LIMIT:
            time_over = True

        time.sleep(1)
        query = build_query(cursor)
        response = make_request(review_url + query)

    save_csv(df_reviews, csv_path)
    return 

def save_progress(idx):
    print('saving progress \n')
    with open('batch.txt', 'w') as batch:
        batch.write('{}'.format(idx))
    print('progress saved \n')
    return

def initialize():
    with open('../get_user_tags/idx_tag.csv', 'r') as doc:
        reader = csv.reader(doc)
        game_ids = []
        for row in reader:
            game_ids.append(row[0])

    with open('batch.txt', 'r') as idx_doc:
        curr_idx = idx_doc.readline()
        # idx_doc holds the index of the last visited entry
        curr_idx = 0 if not curr_idx else int(curr_idx) + 1

    return game_ids, curr_idx

if __name__ == '__main__':
    game_ids, curr_idx = initialize()
    for i in range(curr_idx, len(game_ids)):
        fetch_review(game_ids[i])
        # we save the previous index
        save_progress(i)
        if time_over: 
            break

# fetch_review('1254120')
