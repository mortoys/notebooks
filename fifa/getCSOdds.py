import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def getFile(exid, num=2):
    f = open('cs'+str(num) + '/'+exid+'.html')
    html = f.read()
    f.close()
    return html

def getAttr(b):
    score = b.select_one('strong').text
    odd = b.select_one('.avg.nowrp').text
    
    return score, odd

def visable(b):
    return b.select_one('.odds-cnt').text != '(0)'
    
def getData(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one('#odds-data-table')
    rows = table.select('.table-container .table-header-light')
    return pd.DataFrame([getAttr(row) for row in rows if visable(row)])

def getHalfResult(html):
    soup = BeautifulSoup(html, "html.parser")
    try:
        result = soup.select_one('#event-status .result').text
        r1 = result[result.find('result')+7: result.find(' ', result.find(':'))]
        r2 = result[result.find('(')+1: result.find(', ')]
        r3 = result[result.find(', ')+2: result.find(', ')+5]
        return r1, r2 ,r3
    except:
        return None,None,None

# html = getFile('0AaUjfun')
# getHalfResult(html)
# data = getData(html)

'xeid','date','time','score','win','tie','los','result','team1','team2','usable','s1','s2'