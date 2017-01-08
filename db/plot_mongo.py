#!/usr/bin/env python

from pymongo import MongoClient
import numpy as np
from subprocess import Popen, PIPE, call
import time, datetime
import re
import matplotlib.pyplot as plt
import monary

plt.ion()

# # open database
# client = MongoClient('localhost', 27017)
# db = client['noaa']
# coll = db['data']

# bouldertemp = coll.find(projection={'_id':False, 'ts':True, 'TEMP':True})

# for temp in bouldertemp:
#   print(temp)

#   with monary
monary_connection = monary.Monary(port=27017)


arrays = monary_connection.query(
  db='noaa',
  coll='data',
  query={},
  sort='ts',
  # Timestamp, lon, lat, air temperature.
  fields=['ts', 'TEMP'],
  types=['date', 'int8'])

ts, temp = arrays

plt.plot(ts,temp)

monary_connection.close()
