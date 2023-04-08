import os
import sys
import json as j

json = dict()

directory = os.fsencode(r'2nd_Task/lemmas')

for file in os.listdir(directory):
    filename_without_ext = file.decode("utf-8").split('.')[0]
    _, number = filename_without_ext.split('_')

    if number > '0':
        with open(rf'2nd_Task/lemmas/lemmas_{number}.txt', 'r', encoding='utf-8') as file:
            data = file.read()

    for word in data.split():
        if word in json:
            if not json.get(word).__contains__(number):
                json.get(word).append(number)
        else:
            json[word] = [number]

with open(rf'index.json', 'w', encoding='utf-8') as file:
    j.dump(json, file, ensure_ascii=False)