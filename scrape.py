import json
from pprint import pprint
from multiprocessing import pool
import pandas as pd
import re
import sys
import os

fs = os.listdir('out/html')
fs = [f for f in fs if f.endswith('.html')]

def doit(f):
    fname = f'out/html/{f}'
    ident = f.replace('.html', '')
    outname = f'out/data/{ident}.json'
    try:
        dfs = pd.read_html(fname)
    except ValueError:
        print(f'{ident} has no tables, skipping')
        return

    s = dfs[2][1][8]
    p = r'Grade Span: \(grades (\w*)\s*-\s*(\w*)\).*'
    m = re.match(p, s)
    if m is None:
        print(f'No type for {ident}')
        low = '-'
        high = '-'
    else:
        low = m.groups()[0]
        high = m.groups()[1]

    string = dfs[5][0][1].replace('\xa0', ' ')
    patt = r'^.*Locale: (.*):.*Magnet:\s*(Yes|No)\s*Title I School:\s*(Yes|No).*$'
    m = re.match(patt, string)
    if m is None:
        locale, magnet, title1 = '-', '-', '-'
    else:
        locale, magnet, title1 = m.groups()

    try:
        STR = dfs[5][10][1]
    except:
        STR = '-'

    try:
        ST = dfs[5][4][1]
        if ST == 0:
            raise ValueError('awjfkls')
    except:
        print(f'Cannot process for {ident} (student # not found), skipping')
        return


    rdf = dfs[12]
    races = {}
    for race, count in zip(rdf.iloc[0], rdf.iloc[1]):
        try:
            if count == '–':
                races[race] = 0
            else:
                races[race] = int(count)
        except ValueError:
            pass


    s = dfs[2][2][6]
    m = re.match(r'Charter:(.*)', s)
    if m is None:
        charter = '-'
    else:
        charter = m.groups()[0]

    try:
        black_prop = races['Black'] / ST
        hisp_prop = races['Hispanic'] / ST
        white_prop = races['White'] / ST
    except KeyError:
        print(f'Skipping {ident}, black/hispanic/white not found')
        return

    data = {
        'id': ident,
        'charter': charter.lower(),
        'magnet': magnet.lower(),
        'title1': title1,
        'locale': locale,
        'black': black_prop,
        'hisp': hisp_prop,
        'white': white_prop,
        'str': STR,
        'students': ST,
        'low': low,
        'high': high
    }

    with open(f'out/data/{ident}.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f'{ident} done')


p = pool.Pool(12)
p.map(doit, fs)
print('Done')
