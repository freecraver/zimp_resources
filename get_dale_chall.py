import os
import sys

import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'https://readabilityformulas.com/articles/dale-chall-readability-word-list.php'
TARGET_FILE = 'dictionaries/dale_chall.csv'

if __name__ == '__main__':

    if os.path.exists(TARGET_FILE):
        print(f'{TARGET_FILE} already exists. Cancelling execution')
        sys.exit(-1)

    r = requests.get(DOWNLOAD_URL, headers={"User-Agent": "not_blocked"})
    soup = BeautifulSoup(r.content, features='html.parser')

    word_tables = soup.findAll('table', {'class': 'article_wordlist'})

    words = []
    for tab in word_tables:
        words.extend(sum([td.text.split() for td in tab.findAll('td')], []))

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write('# Original Source:\n')
        f.write(f'# {DOWNLOAD_URL}\n')
        f.writelines('\n'.join(words))
