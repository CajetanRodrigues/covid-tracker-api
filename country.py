import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

headers = {'User-Agent': 'Mozilla/5.0'}
page = requests.get("https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data", headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find_all('table',{'class':['wikitable', 'plainrowheaders', 'sortable', 'jquery-tablesorter']})
# print(table)
# print(len(table))
table_data = table[0].find_all("tr")
# print(len(table_data))

globalData = table_data[1].find_all("th")
    
confirmed = globalData[1].text
deaths = globalData[2].text
recovered = globalData[3].text

globalCases = {}
globalCases["confirmed"] = globalData[1].text.replace("\n","")
globalCases["deaths"] = globalData[2].text.replace("\n","")
globalCases["recovered"] = globalData[3].text.replace("\n","")
globalCases["name"] = "Global"
globalCases["timestamp"] = str(datetime.date(datetime.now()))
# print(globalCases)

# print(table_data[0:len(table_data)-2])
table_data = table_data[0:len(table_data)-2]
globalArray = []
globalArray.append(globalCases)
for i in range(2,len(table_data)):
    temp = {}
    thArray = table_data[i].find_all("th")
    # print(thArray)
    temp["Location"] = thArray[1].a.text
    
    tdArray = table_data[i].find_all("td")
    # print(tdArray)
    temp["confirmed"] = tdArray[0].text.replace("\n","")
    temp["deaths"] = tdArray[1].text.replace("\n","")
    temp["recovered"] = tdArray[2].text.replace("\n","")
    temp["timestamp"] = str(datetime.date(datetime.now()))
    globalArray.append(temp)
    # print(temp)

print(globalArray)

# tdArray = []
# for i in range(len(table_data)):
#     for td in table_data[i].find_all("td"):
#         print(td)
# print(table_data)
# for x in table:
#     print("\n\n\n")
#     print(x)