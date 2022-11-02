import json
import os

id_list = []
with open(os.getcwd() + '\\ginventory_short.json', 'r', encoding='utf-8') as inv:
    parsed = json.load(inv)

for entry in parsed['data']:
    if entry['type'] == 'gin':
        id_list.append(entry['id'])

print(len(id_list))