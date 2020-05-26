import requests
from bs4 import BeautifulSoup
import pandas as pd
headers = {'User-Agent': 'Mozilla/5.0'}
page = requests.get("https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Maharashtra", headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find_all('table',{'class':['wikitable', 'plainrowheaders', 'sortable', 'jquery-tablesorter']})
table = table[1]
# print(table)
table_data = table.tbody.find_all("tr")
table_data = table_data[1:len(table_data)-2]
# print(table_data)
data = []

for i in range(len(table_data)):
    for td in table_data[i].find_all("td"):
        data.append(td.text.replace('\n', ' ').strip())
        print(td.text.replace('\n', ' ').strip())
# print(data)
# del data[4]
    
headers = []
for i in range(len(table_data)):
    temp = []
    for th in table_data[i].find_all("th"):
      if th.a is not None:
        temp.append(th.a.get_text())    # The problem is here, I m not able to get the inner content of 'a' tag. Not able to do th.a.text
    headers.append(temp)
# print(headers)
del headers[4]
rows = []
idx = 0
idx1 = 0
idx2 = 3
while True :
    if(idx2>len(data)):
        break
    row = []
    row = row + headers[idx]
    row = row + data[idx1:idx2]
    rows.append(row)
    idx+=1
    idx1+=4
    idx2+=4

finalArray = []
for row in rows[0:len(rows)-2]:
    print(row)
    temp = {}
    temp["name"] = row[0]
    temp["totalCases"] = row[1]
    temp["recovered"] = row[2]
    temp["deaths"] = row[3]
    finalArray.append(temp)
print(finalArray)