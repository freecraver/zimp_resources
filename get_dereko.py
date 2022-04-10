import os
import sys

import pandas as pd
import requests
import shutil

DOWNLOAD_URL = 'http://www.ids-mannheim.de/fileadmin/kl/derewo/DeReKo-2014-II-MainArchive-STT.100000.freq.zip'
TARGET_FILE = 'word_frequencies/top_10000_de.csv'

if __name__ == '__main__':

    if os.path.exists(TARGET_FILE):
        print(f'{TARGET_FILE} already exists. Cancelling execution')
        sys.exit(-1)

    r = requests.get(DOWNLOAD_URL)
    with open('word_frequencies/tmp.zip', 'wb') as f:
        f.write(r.content)

    shutil.unpack_archive('word_frequencies/tmp.zip', 'word_frequencies/tmp')

    df = pd.read_csv('word_frequencies/tmp/DeReKo-2014-II-MainArchive-STT.100000.freq', sep='\t', header=None)

    with open(TARGET_FILE, 'w') as f:
        f.write('# Original Source:\n')
        f.write('#Institut für Deutsche Sprache (2014): Korpusbasierte Wortformenliste DeReWo, '
                'DeReKo-2014-II-MainArchive-STT.100000\n'
                '#http://www.ids-mannheim.de/derewo, Institut für Deutsche Sprache, Programmbereich Korpuslinguistik,'
                ' Mannheim, Deutschland\n')
        df.loc[:10000, 0].to_csv(f, header=False, index=False, line_terminator='\n')

    shutil.rmtree('word_frequencies/tmp')
    os.remove('word_frequencies/tmp.zip')