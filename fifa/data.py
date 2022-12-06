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

dd[
    ['xeid','date','time','score','s1','s2','win','tie','los','result','usable','team1','team2']
].to_csv('fifa2022.csv', index=None)



def getY(xeid, yy):
    tt = yy.set_index(0)
    tt.index.name = 'score'
    tt.columns = [xeid]
    return tt

xeid = dd[dd['usable']]['xeid']
y = pd.DataFrame()
for i in range(len(xeid)):
    iid = xeid.iloc[i]
    uu = getY(iid, getData(getFile(iid, 4)))
    y = pd.merge(y, uu, left_index=True, right_index=True, how='outer')

qq = y.fillna(10000).T
qq = qq.applymap(lambda s: float(s))

qq.to_parquet('cs4.pq')