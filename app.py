from flask import Flask, request 
import json
import requests
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
import pymongo
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)


client = MongoClient('mongodb+srv://admin:admin@cluster0-qbkxj.mongodb.net/test?retryWrites=true&w=majority',27017)
# client=MongoClient('localhost',27017)
db=client.covid
state=db.state
district=db.district

@app.route('/districts', methods = ["GET"])
def getDistricts():
    objects = district.find({"name":"Mumbai City"})
    date = ''
    for x in objects:
        print(x)
        if x["timestamp"]:
            date = x["timestamp"]
    if str(datetime.date(datetime.now())) == str(date):
        response = []
        districtArray = district.find()
        for district_item in districtArray:
            district_item["_id"] = str(district_item["_id"])
            response.append(district_item)
        return json.dumps(response)
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
    for i in range(4,9):
        del headers[4]
    # print(headers)
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
    for row in rows[0:len(rows)-1]:
        temp = {}
        temp["name"] = row[0]
        temp["totalCases"] = row[1]
        temp["recovered"] = row[2]
        temp["deaths"] = row[3]
        temp["timestamp"] = str(datetime.date(datetime.now()))
        finalArray.append(temp)
    district.insert_many(finalArray)
    
    response = []
    districtArray = district.find()
    for district_item in districtArray:
        district_item["_id"] = str(district_item["_id"])
        response.append(district_item)
    return json.dumps(response)

@app.route('/states', methods = ["GET"]) 
def scrapeIndiaStates():
    objects = state.find({"name":"Maharashtra"})
    date = ''
    for x in objects:
        print(x)
        if x["timestamp"]:
            date = x["timestamp"]
    if str(datetime.date(datetime.now())) == str(date):
        response = []
        stateArray = state.find()
        for state_item in stateArray:
            state_item["_id"] = str(state_item["_id"])
            response.append(state_item)
        return json.dumps(response)
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get("https://en.wikipedia.org/wiki/COVID-19_pandemic_in_India", headers=headers)

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
        temp["timestamp"] = str(datetime.date(datetime.now()))
        JsonObjectArray.append(temp)
    state.insert_many(JsonObjectArray)
    response = []
    stateArray = state.find()
    for state_item in stateArray:
        state_item["_id"] = str(state_item["_id"])
        response.append(state_item)
    return json.dumps(response)





if __name__ == '__main__':  
    app.run(host='0.0.0.0',port=8082,debug = True)

