from flask import Flask, request 
import json
import requests
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/global', methods = ["GET"]) 
def getGlobal():
    response = requests.get('https://api.covid19api.com/summary',headers={"Content-Type": "application/json"})
    return json.dumps(response.json()["Global"])

@app.route('/countries', methods = ["GET"]) 
def getCountries():
    response = requests.get('https://api.covid19api.com/summary',headers={"Content-Type": "application/json"})
    return json.dumps(response.json()["Countries"])

if __name__ == '__main__':  
    app.run(host='127.0.0.1',port=80,debug = True)
