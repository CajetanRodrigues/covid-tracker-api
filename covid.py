import requests
from bs4 import BeautifulSoup
import pandas as pd
headers = {'User-Agent': 'Mozilla/5.0'}
page = requests.get("https://en.wikipedia.org/wiki/COVID-19_pandemic_in_India", headers=headers)
# print(page.status_code)

# print(page.content)

soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find('table',{'class':'multicol'})
table_data = table.tbody.find_all("tr")
data = []
for td in table_data[0].find_all("td"):
    data.append(td.text.replace('\n', ' ').strip())

data = data[1:len(data)]
del data[len(data)-1]
# print(data)
data2 = []
for th in table_data[0].find_all("th"):
    data2.append(th.text.replace('\n', ' ').strip())

data2 = data2[7:len(data2)]

# print(data2)
rows = []
idx1 = 0
idx2 = 1

idx3 = 0
idx4 = 3
while True:
    if(idx4>len(data)):
        break
    tempArray = [] 
    data3idx = 0
    tempArray= tempArray + data[idx3:idx4+1]
    tempArray = tempArray + data2[idx1:idx2+1]
    rows.append(tempArray)
    idx1+=2
    idx2+=2
    
    idx3+=4
    idx4+=4
# print(rows)

JsonObjectArray = []
for row in rows:
    temp = {}
    
    temp["totalCases"] = row[0]
    temp["deaths"] = row[1]
    temp["recoveries"] = row[2]
    temp["activeCases"] = row[3]
    temp["name"] = row[5] 
    JsonObjectArray.append(temp)
print(JsonObjectArray)