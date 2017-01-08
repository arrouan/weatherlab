#!/usr/bin/env python

from flask import Flask
from flask import render_template

from pymongo import MongoClient

import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/noaa/data")

def noaa_data():
  # # open database
  client = MongoClient('localhost', 27017)
  db = client['noaa']
  coll = db['data']
  
  bouldertemp = coll.find(projection={'_id':False, 'ts':True, 'TEMP':True})
  json_temp = []
  for temp in bouldertemp:
    json_temp.append(temp)
  json_temp = json.dumps(json_temp,default=json_util.default)

  client.close()
  return json_temp
  
if __name__ == "__main__":
  app.run(host='0.0.0.0',port=5000,debug=True)
