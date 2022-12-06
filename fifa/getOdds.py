"""
从保存的赔率网页文件中提取数据
"""

from bs4 import BeautifulSoup
import pandas as pd
import datetime

def getFile(index):
    f = open('page/'+str(index)+'.html')
    html = f.read()
    f.close()
    return html

def getAttr(b):
    xeid = b.attrs['xeid']
    timet = b.select_one('.table-time').attrs['class'][2]
    date = datetime.date.fromtimestamp(int(timet[1:11])).isoformat()
    time = b.select_one('.table-time').text
    title = b.select_one('.name.table-participant').text
    score = b.select_one('.table-score').text

    odds = [odd.text for odd in b.select('.odds-nowrp')]
    flag = None
    for i in [0,1,2]:
        if 'result-ok' in b.select('.odds-nowrp')[i].attrs['class']:
            flag = i
    
    return [xeid, date,time,title,score,] + odds + [flag]

def getData(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one('.table-main')
    rows = table.select('tr.deactivate')
    return pd.DataFrame([getAttr(row) for row in rows])

data = pd.DataFrame()
for i in range(18):
    html = getFile(i+1)
    data = pd.concat([data, getData(html)])


data.columns = ['xeid', 'date', 'time', 'teams', 'score', 'win', 'tie', 'los', 'result']

data = data[data['result'] != None]
data = data[data['tie'] != '-']
data = data[data['win'] != '-']
data = data[data['los'] != '-']
data['team1'] = data['teams'].str.split(' - ').apply(lambda s: s[0])
data['team2'] = data['teams'].str.split(' - ').apply(lambda s: s[1])
data = data.drop('teams', axis=1)

data.to_csv('fifa2022.csv', index=False)