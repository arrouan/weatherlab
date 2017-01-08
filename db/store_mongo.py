#!/usr/bin/env python

from pymongo import MongoClient
import numpy as np
from subprocess import Popen, PIPE, call
import time, datetime
import re

ishdir = './'

year = '2016'

dir1 = 'data/' + year + '/'
file1 = '720533-99999-' + year

# open database
client = MongoClient('localhost', 27017)
db = client['noaa']
coll = db['data']


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


NOAA_fields = {
  'USAF':  [0,6],
  'WBAN':  [7,12],
  'TIME':  [13,25], # YYYYMMDDHH
  'DIR':   [26,29], # WIND DIRECTION IN COMPASS DEGREES, 990 = VARIABLE, REPORTED AS '***' WHEN AIR IS CALM (SPD WILL THEN BE 000)
  'SPD':   [30,33], # WIND SPEED IN MILES PER HOUR 
  'GUS':   [34,37], # GUST IN MILES PER HOUR 
  'CLG':   [38,41], # CLOUD CEILING--LOWEST OPAQUE LAYER WITH 5/8 OR GREATER COVERAGE, IN HUNDREDS OF FEET, 722 = UNLIMITED 
  'SKC':   [42,45], # SKY COVER -- CLR-CLEAR, SCT-SCATTERED-1/8 TO 4/8, BKN-BROKEN-5/8 TO 7/8, OVC-OVERCAST, OBS-OBSCURED, POB-PARTIAL OBSCURATION
  'L':     [46,47], # LOW CLOUD TYPE
  'M':     [48,49], # MEDIUM CLOUD TYPE
  'H':     [50,51], # HIGH CLOUD TYPE
  'VSB':   [52,56], # VISIBILITY IN STATUTE MILES TO NEAREST TENTH
  'MW1':   [57,59], # MANUALLY OBSERVED PRESENT WEATHER (see table on website listed above for detail)
  'MW2':   [60,62], #
  'MW3':   [63,65], #
  'MW4':   [66,68], #
  'AW1':   [69,71], # AUTO-OBSERVED PRESENT WEATHER (see table on website listed above for detail)
  'AW2':   [72,74], #
  'AW3':   [75,77], #
  'AW4':   [78,80], #
  'W':     [81,82], # PAST WEATHER INDICATOR
  'TEMP':  [83,87], # TEMPERATURE IN FARENHEIT
  'DEWP':  [88,92], # DEWPOINT IN FARENHEIT
  'SLP':   [93,99], # SEA LEVEL PRESSURE IN MILLIBARS TO NEAREST TENTH
  'ALT':   [100,105], # ALTIMETER SETTING IN INCHES TO NEAREST HUNDREDTH
  'STP':   [106,112], # STATION PRESSURE IN MILLIBARS TO NEAREST TENTH
  'MAX':   [113,116], # MAXIMUM TEMPERATURE IN FAHRENHEIT (TIME PERIOD VARIES)
  'MIN':   [117,120], # MINIMUM TEMPERATURE IN FAHRENHEIT (TIME PERIOD VARIES)
  'PCP01': [121,126], # 1-HOUR LIQUID PRECIP REPORT IN INCHES AND HUNDREDTHS -- THAT IS, THE PRECIP FOR THE PRECEDING 1 HOUR PERIOD
  'PCP06': [127,132], # 6-HOUR LIQUID PRECIP REPORT IN INCHES AND HUNDREDTHS -- THAT IS, THE PRECIP FOR THE PRECEDING 6 HOUR PERIOD
  'PCP24': [133,138], # 24-HOUR LIQUID PRECIP REPORT IN INCHES AND HUNDREDTHS -- THAT IS, THE PRECIP FOR THE PRECEDING 24 HOUR PERIOD
  'PCPXX': [139,144], # LIQUID PRECIP REPORT IN INCHES AND HUNDREDTHS, FOR A PERIOD OTHER THAN 1, 6, OR 24 HOURS (USUALLY FOR 12 HOUR PERIOD FOR STATIONS OUTSIDE THE U.S., AND FOR 3 HOUR PERIOD FOR THE U.S.) T = TRACE FOR ANY PRECIP FIELD
  'SD':    [145,147], # SNOW DEPTH IN INCHES
}

nv = len(NOAA_fields)
storefields = ['USAF', 'WBAN','DIR','SPD', 'GUS', 'CLG','SKC','L','M','H','VSB','MW1','MW2','MW3','MW4','AW1','AW2','AW3','AW4','W','TEMP','DEWP','SLP','ALT','STP','MAX','MIN','PCP01','PCP06','PCP24','PCPXX','SD']


p2 = call(["gunzip",dir1+file1+'.gz'])
p3 = call(['java', '-classpath', ishdir, 'ishJava', dir1+file1, dir1+file1+'.dat' ])
#data = str(p3.communicate()[0]).split("\\n")[1:-1]
#data = p3.communicate()[0]
                

with open(dir1+file1+'.dat' , 'r') as myfile:
  data=myfile.read().split('\n')[1:-1]


si_d = len(data)
new_recs = []
nco = 0
for nd in range(0,si_d):
  new_recs.append({})
  nco = nco + 1
  fld='TIME'
  mdate=data[nd][NOAA_fields[fld][0]:NOAA_fields[fld][1]].strip()
#  new_recs[nd]['ts'] = datetime.datetime.strptime(str(mdate), '%Y%m%d%H%M')
  new_recs[nd]['ts'] = mdate
  for fld in storefields:
    val = data[nd][NOAA_fields[fld][0]:NOAA_fields[fld][1]].strip()
    if not re.search('\*', val):
      if fld == "SKC":
        new_recs[nd][fld] = val
      else:
        new_recs[nd][fld] = num(val)
      
result = coll.insert_many(new_recs)
