import pandas as pd
import json


with open('number.json', 'r') as r:
    search = json.load(r)

s = search[7000:7100]
a = pd.read_csv('Result.csv', delimiter=',', encoding='utf-8')
b = list(a['箱号'].drop_duplicates())

ii = 0
with open('early_error.csv', 'w') as w:
    for i in s:
        ii += 1
        if i in b:
            continue
        else:
            print(ii)
            w.write('"%s",\n' % i)
