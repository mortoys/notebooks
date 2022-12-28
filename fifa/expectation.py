import pandas as pd
import numpy as np

# cs2
cs = pd.read_parquet('cs2.pq')
r = (1/cs).T.sum().mean()

oo = cs.columns.str.split(':').to_series().apply(lambda s: s[0] == '0')
e1 = -np.log((1/cs.iloc[:,list(oo)]/r).T.sum())

oo = cs.columns.str.split(':').to_series().apply(lambda s: s[1] == '0')
e2 = -np.log((1/cs.iloc[:,list(oo)]/r).T.sum())

e1.name = 't1e'
e2.name = 't2e'

te = pd.merge(e1, e2, left_index=True, right_index=True)


# cs3
cs = pd.read_parquet('cs3.pq')
r = (1/cs).T.sum().mean()

oo = cs.columns.str.split(':').to_series().apply(lambda s: s[0] == '0')
e1 = -np.log((1/cs.iloc[:,list(oo)]/r).T.sum())

oo = cs.columns.str.split(':').to_series().apply(lambda s: s[1] == '0')
e2 = -np.log((1/cs.iloc[:,list(oo)]/r).T.sum())

e1.name = 'h11e'
e2.name = 'h12e'

h1e = pd.merge(e1, e2, left_index=True, right_index=True)

# cs4
cs = pd.read_parquet('cs4.pq')
r = (1/cs).T.sum().mean()

oo = cs.columns.str.split(':').to_series().apply(lambda s: s[0] == '0')
e1 = -np.log((1/cs.iloc[:,list(oo)]/r).T.sum())

oo = cs.columns.str.split(':').to_series().apply(lambda s: s[1] == '0')
e2 = -np.log((1/cs.iloc[:,list(oo)]/r).T.sum())

e1.name = 'h21e'
e2.name = 'h22e'

h2e = pd.merge(e1, e2, left_index=True, right_index=True)

# expectation

expectation = pd.merge(te,
    pd.merge(h1e, h2e, left_index=True, right_index=True)
     , left_index=True, right_index=True)

expectation.index.name = 'xeid'

expectation.to_csv('expectation.csv')