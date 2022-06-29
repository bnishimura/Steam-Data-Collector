These are quick little one-time scripts I wrote to fetch and process data.
The following scripts have been executed in order:

first you request app_list.json from 
http://api.steampowered.com/ISteamApps/GetAppList/v0002

parse_list.py: 
    cleans the names of the games, removing unicode from names. 
    Produces app_list.csv

append_api_data.py: 
    fetches data from the following api:
    https://store.steampowered.com/api/appdetails/?json=1&appids=
    and appends some data (like price, release date, and stuff) to app_list.csv. 
    we save progress using batch_info.txt (if someone wants to use this
    script, set batch_info to 0)
    THIS TAKES DAYS
