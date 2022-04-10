import os
import sys
import pandas as pd
import requests

DOWNLOAD_URL = 'https://ucrel.lancs.ac.uk/bncfreq/lists/1_2_all_freq.txt'
TARGET_FILE = 'word_frequencies/top_10000_en.csv'

if __name__ == '__main__':

    if os.path.exists(TARGET_FILE):
        print(f'{TARGET_FILE} already exists. Cancelling execution')
        sys.exit(-1)

    r = requests.get(DOWNLOAD_URL)
    with open('word_frequencies/tmp.txt', 'w', encoding='utf-8') as f:
        # original files is broken and contains some specific rules we don't care about
        txt = '\n'.join([line.strip().replace('*', '').replace('~', '') for line in r.text.split('\n')])
        f.writelines(txt)

    df = pd.read_csv('word_frequencies/tmp.txt', sep='\t')

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write('# Original Source:\n')
        f.write('# https://ucrel.lancs.ac.uk/bncfreq/lists/1_2_all_freq.txt\n')
        df.loc[:10000, ['Word']].to_csv(f, header=False, index=False, line_terminator='\n')

    os.remove('word_frequencies/tmp.txt')
