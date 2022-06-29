'''
This script simply opens a json dump from 
http://api.steampowered.com/ISteamApps/GetAppList/v0002
and formats it into a csv file following the format
    | appid | name |
1   | _id_  | xxxx |

The script is isolated because of the one time only nature of the process.
'''
import json
import csv
from operator import itemgetter


with open('app_list.json', 'r') as appList, open('app_list.csv', 'w') as output:
    str_data = json.load(appList)
    data = json.loads(str_data)
    game_list = data['applist']['apps']

    writer = csv.DictWriter(output, fieldnames=['appid', 'name'], lineterminator='\n')
    writer.writeheader()

    for i in range(len(game_list)):
        appid, name = itemgetter('appid', 'name')(game_list[i])
        # encode to ascii to make chinese characters and stuff disappear
        # decode back do utf-8 so the name appears as a string instead of a byte string
        # on the csv
        encoded = name.encode('ascii', 'ignore').decode('utf-8')

        writer.writerow({'appid': appid, 'name': encoded})
