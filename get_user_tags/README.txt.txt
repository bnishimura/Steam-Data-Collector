Fetches user tags from the steam store page.
These scripts are executed in order:

chop_tbl.py: 
    opens app_list.csv and takes only the 'game_id' column.
    Saves the column to idx_tag.csv

get_user_tags.py:
    looks at idx_tag.csv and fetches steam pages only for ids that have type
    'game'. Extends rows from idx_tag.csv with scraped data from steam pages.
    uses tag_batch_info.txt to save progess 
    TAKES DAYS TO COMPLETE
