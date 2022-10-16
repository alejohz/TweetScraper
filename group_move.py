from pathlib import Path
import json
from typing import List
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path_to_save")
args = parser.parse_args()

p = Path('.')
tweets = [file for file in (p / 'data' / 'tweet').rglob('*') if file.is_file()]
# users = [file for file in (p / 'data' / 'user').rglob('*') if file.is_file()]


def merge_group(file_list: List, file_name: str):
    data = []
    for f in file_list:
        with open(f, 'r') as in_file:
            data.append(json.load(in_file))

    with open(p / 'output' / file_name, 'a') as outfile:
        json.dump(data, outfile)


merge_group(tweets, "rappi_tweets.json")
# merge_group(users, f"Viva_Env_users_merged.json")

shutil.rmtree(p / 'data' / 'tweet')
shutil.rmtree(p / 'data' / 'user')
