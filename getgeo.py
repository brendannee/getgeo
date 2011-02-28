#!/usr/bin/env python
# encoding: utf-8
"""
getgeo.py

Created by Jedidiah Horne on 2011-02-26.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import csv
import re
import simplegeo.context
import ConfigParser

def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False

    return True
    
def getTiger(county, state):
  counties = csv.reader(open("county_fips.txt",'r'))
  states = csv.reader(open("state_fips.txt",'r'))

  county_clean = re.sub(' ','_',county)

  for s in states:
    if s[0] == state.upper() or s[2] == state.upper():
      state_fips = s[1]
      state = s[2]
      state_code = s[0]
      state_clean = re.sub(' ','_',s[2])
      break
  for c in counties:
    if re.sub(' ','_',c[1].lower()) == county_clean.lower() and state_fips == c[0][:2]:
      county_fips = c[0]
  try:
    print "County fips code: %s" % county_fips
  except UnboundLocalError:
    print 'County name not found for "'+county+', '+state+'".  Please try again.'
    sys.exit(1)
    
  url = "http://www2.census.gov/geo/tiger/TIGER2009/%s_%s/%s_%s_County/tl_2009_%s_edges.zip" % (state_fips,state_clean,county_fips,county_clean,county_fips)
  print "Retrieving Tiger data for " + county + " County in " + state
  print url
  os.system('curl %s > %s_%s_edges.zip' % (url,county_clean,state_code))
  os.system('sudo chown $USER %s_%s_edges.zip' % (county_clean,state_code))
  os.system('unzip %s_%s_edges.zip -d %s_%s' % (county_clean,state_code,county_clean,state_code))
  os.system('rm %s_%s_edges.zip' % (county_clean,state_code))
#http://www2.census.gov/geo/tiger/TIGER2009/06_CALIFORNIA/06001_Alameda_County/tl_2009_06001_edges.zip

def main():
  # Check if number to see if a coordinate
  if is_number(sys.argv[1]):
    if len(sys.argv)<3:
      print 'Missing second argument for Coordinates.  Please enter a Count Name and State abbreviation or a latitide longitude pair ex: "La Crosse" WI or 37.775 -122.4183333'
      sys.exit(1)
    lat = float(sys.argv[1])
    lng = float(sys.argv[2])

    config = ConfigParser.RawConfigParser()
    config.read('keys.cfg')

    client = simplegeo.context.Client(config.get('SimpleGeo', 'simplegeokey'), config.get('SimpleGeo', 'simplegeosecret'))
    context = client.get_context(lat,lng)
    
    for f in context['features']:
      if f['classifiers'][0]['subcategory'] == 'County':
        county = f['name']
      elif f['classifiers'][0]['subcategory'] == 'State':
        state = f['name']
    getTiger(county,state)
    
  else:
    # Check if a county and state have been passed
    if len(sys.argv)<3:
      print 'Missing second argument for Coordinates.  Please enter a Count Name and State abbreviation or a latitide longitude pair ex: "La Crosse" WI or 37.775 -122.4183333'
      sys.exit(1)
      
    county = sys.argv[1]
    state = sys.argv[2]
    getTiger(county,state)


if __name__ == '__main__':
  main()

