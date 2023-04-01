import os
import requests
from bs4 import BeautifulSoup

sites = [
    'https://www.mk.ru'
]
links = []

for i in sites:
    if not links.__contains__(i):
        links.append(i)

count = 0
i = 0

if not os.path.exists(fr'texts'):
    os.makedirs(fr'texts')

while count < 100:
    if links[i] is not None:
        if not links[i].__contains__('http'):
            i += 1
            continue
        current_website = links[i]
        i += 1
    else:
        break

    try:
        request = requests.get(current_website)
    except:
        print(f'Error: {current_website}')
        continue

    soup = BeautifulSoup(request.text, 'lxml')
    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    parts = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in parts if chunk)

    num_words = len(text.split())

    all_a = soup.find_all('a')

    for a in all_a:
        if not links.__contains__(a.get('href')):
            links.append(a.get('href'))

    if num_words >= 1000:
        count += 1
        with open(f"texts/{count}.txt", "w", encoding="utf-8") as myfile:
            myfile.write(text)
            myfile.close()
        with open(fr"index.txt", "a") as myfile:
            myfile.write(f"{count}.txt -> {current_website}\n")
    print(count)