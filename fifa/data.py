from getCSOdds import getFile, getData, getHalfResult
import pandas as pd

dd = pd.read_csv('fifa2022.csv')

import os

fl = pd.Series(list(set(os.listdir('./cs2')) & set(os.listdir('./cs3')) & set(os.listdir('./cs4'))))\
.apply(lambda s: s[:8])

dd['usable'] = dd['xeid'].isin(fl)

a = dd[dd['usable']]['xeid'].apply(lambda s: getHalfResult(getFile(s, 3)))
dd['s1'] = a.apply(lambda s: s[1])
dd['s2'] = a.apply(lambda s: s[2])

dd = dd[
    ['xeid','date','time','score','h1','h2','win','tie','los','result','usable','team1','team2']
]

h1 = dd['h1'].str.split(':').apply(pd.Series)
h1.columns = ['h11', 'h12']
h2 = dd['h2'].str.split(':').apply(pd.Series)
h2.columns = ['h21', 'h22']

def can_convert_to_int(string):
    try:
        int(string)

        return True
    except ValueError:
        return False

check1 = h1.applymap(can_convert_to_int)
check2 = h2.applymap(can_convert_to_int)

dd['usable'] = dd['usable'] & (check1.T.sum() == 2) & (check2.T.sum() == 2)

dd = pd.concat([dd, h1, h2], axis=1)

dd['h11'] = pd.to_numeric(dd['h11'], errors='coerce')
dd['h12'] = pd.to_numeric(dd['h12'], errors='coerce')
dd['h21'] = pd.to_numeric(dd['h21'], errors='coerce')
dd['h22'] = pd.to_numeric(dd['h22'], errors='coerce')

dd['t1'] = dd['h11'] + dd['h21']
dd['t2'] = dd['h12'] + dd['h22']

dd.to_csv('fifa2022.csv', index=None)


# def getY(xeid, yy):
#     tt = yy.set_index(0)
#     tt.index.name = 'score'
#     tt.columns = [xeid]
#     return tt

# xeid = dd[dd['usable']]['xeid']
# y = pd.DataFrame()
# for i in range(len(xeid)):
#     iid = xeid.iloc[i]
#     uu = getY(iid, getData(getFile(iid, 3)))
#     y = pd.merge(y, uu, left_index=True, right_index=True, how='outer')

# qq = y.fillna(10000).T
# qq = qq.applymap(lambda s: float(s))

# qq.to_parquet('cs3.pq')