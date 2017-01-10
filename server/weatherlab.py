#!/usr/bin/env python

from flask import Flask
from flask import render_template

from influxdb import InfluxDBClient

import json

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/noaa/data")

def noaa_data():
  # # open database
  dbname='noaa'

  client = InfluxDBClient(database=dbname, host="influx")

  query = 'select TEMP from boulder;'
  result = client.query(query)
  json_res = list(result.get_points(measurement='boulder'))
  json_temp = json.dumps(json_res)

  return json_temp



if __name__ == "__main__":
  app.run(host='0.0.0.0',port=5000,debug=True)
