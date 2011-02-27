#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Jedidiah Horne on 2011-02-26.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import csv
import re

def main():
  county = re.sub(' ','_',sys.argv[1])
  state = sys.argv[2]
  
  counties = csv.reader(open("county_fips.txt",'r'))
  states = csv.reader(open("state_fips.txt",'r'))
  
  for s in states:
    if s[0] == state:
      state_fips = s[1]
      state_full = re.sub(' ','_',s[2])
      break
  
  for c in counties:
    if re.sub(' ','_',c[1].lower()) == county.lower() and state_fips == c[0][:2]:
      county_fips = c[0]
  try:
    print "County fips code: %s" % county_fips
  except UnboundLocalError:
    print "County name not found.  Please try again."
    sys.exit(1)
  url = "http://www2.census.gov/geo/tiger/TIGER2009/%s_%s/%s_%s_County/tl_2009_%s_edges.zip" % (state_fips,state_full,county_fips,county,county_fips)
  os.system('curl %s > %s_%s_edges.zip' % (url,county,state))
  os.system('sudo chown $USER %s_%s_edges.zip' % (county,state))
  os.system('unzip %s_%s_edges.zip -d %s_%s' % (county,state,county,state))
  os.system('rm %s_%s_edges.zip' % (county,state))
  print url
#http://www2.census.gov/geo/tiger/TIGER2009/06_CALIFORNIA/06001_Alameda_County/tl_2009_06001_edges.zip


if __name__ == '__main__':
  main()

