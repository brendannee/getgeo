#!/usr/bin/env python
# encoding: utf-8
"""
getgeo.py

Created by Jedidiah Horne on 2011-02-26.
Copyright (c) 2011 __BlinkTag Inc__. All rights reserved.
"""
usage =  """\tgetgeo [latitude] [longitude]\n\tgetgeo [County] [State]\n\tgetgeo [City] [State]\n\nExamples:\n\tgetgeo 36.5678 -120.678\n\tgetgeo "New Orleans" LA\n\tgetgeo Alameda CA"""

import sys
import os
import csv
import re
import simplejson
import ConfigParser
import simplegeo.context


def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False

    return True

def getFips(county,state):
  output = {}
  counties = csv.reader(open("county_fips.txt",'r'))
  states = csv.reader(open("state_fips.txt",'r'))

  county_clean = re.sub(' ','_',county).title()

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
    print "County found: %s, %s Fips code: %s" % (county, state, county_fips)
    
    output['county_fips'] = county_fips
    output['county_clean'] = county_clean
    output['county'] = county.title()
    output['state'] = state.title()
    output['state_fips'] = state_fips
    output['state_code'] = state_code
    output['state_clean'] = state_clean
    return output
  except UnboundLocalError:
    print 'County name not found for "'+county+', '+state+'".'
    return 'false'

def getTiger(county_info):
  
  file_list = ['edges','areawater','arealm','pointlm','faces','tabblock10','tabblock00','bg10','bg00','tract10','tract00','cousub10','cousub00','vtd10','vtd00','addrfn','addr','featnames','otherid','facesah','facesal']
  #file_list = ['edges']
  print "----------Retrieving Tiger data for " + county_info['county'] + " County in " + county_info['state']
  for i in file_list:  
    if county_info['state_code'] <> 'LA':
      url = "http://www2.census.gov/geo/tiger/TIGER2009/%s_%s/%s_%s_County/tl_2009_%s_%s.zip" % (county_info['state_fips'],county_info['state_clean'],county_info['county_fips'],county_info['county_clean'],county_info['county_fips'],i)
    else:
      url = "http://www2.census.gov/geo/tiger/TIGER2009/%s_%s/%s_%s_Parish/tl_2009_%s_%s.zip" % (county_info['state_fips'],county_info['state_clean'],county_info['county_fips'],county_info['county_clean'],county_info['county_fips'],i)
    print "File: tiger_%s" % i
    print url
    os.system('curl -silent %s > %s_%s_%s.zip' % (url,county_info['county_clean'],county_info['state_code'],i))
    os.system('sudo chown $USER %s_%s_%s.zip' % (county_info['county_clean'],county_info['state_code'],i))
    os.system('unzip %s_%s_%s.zip -d %s_%s' % (county_info['county_clean'],county_info['state_code'],i,county_info['county_clean'],county_info['state_code']))
    os.system('rm %s_%s_%s.zip' % (county_info['county_clean'],county_info['state_code'],i))

def get_osm(x,y,county_info):
  box_width = .25
  print "----------Gathering largest possible OSM bounding box around point."
  while box_width > 0:
    print "Attempting %s degree box" % (box_width * 2)
    url = "http://api.openstreetmap.org/api/0.6/map?bbox=%s,%s,%s,%s" % (float(x)-box_width,float(y)-box_width,float(x)+box_width,float(y)+box_width)
    os.system('curl %s > ./%s_%s/%s_%s_osm.xml' % (url,county_info['county_clean'],county_info['state_code'],county_info['county_clean'],county_info['state_code']))
    f = open('./%s_%s/%s_%s_osm.xml' % (county_info['county_clean'],county_info['state_code'],county_info['county_clean'],county_info['state_code']))
    if len(f.readlines()) < 10:
      print "Too many nodes.  Retrying..."
    else:
      print "Sucessfully downloaded OSM %s box around %s County, %s" % (box_width * 2, county_info['county_clean'], county_info['state_code'])
      break
    box_width = box_width - .01

def main():
  
  # strip off trailing comma of first argument
  sys.argv[1] = re.sub(',','',sys.argv[1])
  
  #Setup simplegeo client
  config = ConfigParser.RawConfigParser()
  config.read('keys.cfg')
  try:
    client = simplegeo.context.Client(config.get('SimpleGeo', 'simplegeokey'), config.get('SimpleGeo', 'simplegeosecret'))
  except ConfigParser.NoSectionError:
    print "error: Cannot find file keys.cfg with valid SimpleGeo Keys.  Please add your SimpleGeo API keys to keys.cfg and run the deploy script again"
    sys.exit(1)
    
  if (sys.argv[1] == ''):
    print "usage: \n%s" % usage
    sys.exit(1)
  
  # Check if number to see if a coordinate
  if is_number(sys.argv[1]):
    if len(sys.argv)<3:
      print 'Missing second argument for Coordinates.  Please enter a County Name and State abbreviation or a latitide longitude pair ex: "New Orleans" LA or 37.775 -122.4183333'
      sys.exit(1)
    lat = float(sys.argv[1])
    lng = float(sys.argv[2])
    
    # Get info from SimpleGeo
    context = client.get_context(lat,lng)

  else:
    # Check if a county and state have been passed or city and state
    if len(sys.argv)<3:
      print 'Missing second argument for State.  Please enter a County Name and State abbreviation or a latitide longitude pair ex: "New Orleans" LA or 37.775 -122.4183333'
      sys.exit(1)
    
    # Get info from SimpleGeo
    context = client.get_context_by_address(sys.argv[1] + ', ' + sys.argv[2])
  
  # Loop through SimpleGeo Results
  for f in context['features']:
    if f['classifiers'][0]['subcategory'] == 'County':
      county = f['name']
    elif f['classifiers'][0]['subcategory'] == 'State':
      state = f['name']
  lat = context['query']['latitude']
  lng = context['query']['longitude']
  
  county_info = getFips(county,state)
  
  if county_info == 'false':
    print "County/State or City/State pair not found."
    sys.exit(1)
    
  # Remove any existing county info and make new directory
  os.system('rm -rf %s_%s' % (county_info['county_clean'],county_info['state_code']))
  os.system('mkdir %s_%s' % (county_info['county_clean'],county_info['state_code']))
  try:
    # Save SimpleGeo Context response
    f = open('./%s_%s/%s_%s_simplegeo_context.json' % (county_info['county_clean'],county_info['state_code'],county_info['county_clean'],county_info['state_code']), 'w')
    f.write(simplejson.dumps(context, f, use_decimal=True))
    
    getTiger(county_info)
    get_osm(lng,lat,county_info)
  except UnboundLocalError:
    print "County/State or City/State pair not found."
    sys.exit(1)  

if __name__ == '__main__':
  main()

