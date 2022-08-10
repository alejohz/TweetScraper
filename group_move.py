from pathlib import Path
import json
from typing import List
import shutil
# United States, Germany, Spain, Japan, Egypt, South Africa, Turkey
country = 'united states'
p = Path('.')
tweets = [file for file in (p / 'Data' / 'tweet').rglob('*') if file.is_file()]
users = [file for file in (p / 'Data' / 'user').rglob('*') if file.is_file()]

def merge_group(file_list:List, file_name:str):
    data = []

    for f in file_list:
        with open(f, 'r') as infile:
            data.append(json.load(infile))

    with open(p / 'Output' / file_name,'w') as outfile:
        json.dump(data, outfile)

merge_group(tweets, f"{country} tweets_merged.json")
merge_group(users, f"{country} users_merged.json")

shutil.rmtree(p / 'Data'/ 'tweet')
shutil.rmtree(p / 'Data'/ 'user')
