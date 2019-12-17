import os
import pandas as pd
import json
with open('shootingids.json') as f:
    sids = set(json.load(f))
    print(len(sids))
    sids = {sid for sid in sids if len(sid) == 12}
    print(len(sids))

fs = os.listdir('out/data')
ds = []
for f in fs:
    fpath = f'out/data/{f}'
    ident = f.replace('.json', '')
    with open(fpath) as fh:
        dat = json.load(fh)
        dat['shooting'] = dat['id'] in sids
        ds.append(dat)

df = pd.DataFrame(ds)
df.to_csv('collected.tsv', sep='\t', index=False)
print('Done')
