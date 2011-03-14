getgeo
=========

getgeo is a python script that downloads Tiger and OSM data for specified location.  It takes a pair of coordinates, a county/state or a city/state as arguments, uses the [SimpleGeo Context API](http://simplegeo.com/docs/api-endpoints/simplegeo-context) to determine what county this point is in and downloads, unzips and renames [Tiger](https://www.census.gov/geo/www/tiger/) and [OpenStreetMap (OSM)](http://www.openstreetmap.org/) data.

For OSM data, it tries to get data for the largest possible bounding box around the specified point, but is limited to the maximum download size permitted by OSM.

Installation Notes
----------------------------

- [Install simplegeo.context python client](http://simplegeo.com/docs/clients-code-libraries/python#installation-and-requirements)
- [Get a SimpleGeo API key](http://simplegeo.com/signup/)
- Put the SimpleGeo  OAuth Key and SecretKey in the file keys_sample.cfg and rename it to keys.cfg
- To install getgeo run $ sudo sh deploy.sh - this copies it to your path and puts the getgeo files somewhere so you can execute "getgeo" at the command line


Example Usage
----------------------------

#### Coordinates
$ getgeo 36.5678 -120.678

#### City and State
$ getgeo "New Orleans" LA

#### County and State
$ getgeo Alameda CA


APIs used
----------------------------
- [SimpleGeo Context API](http://simplegeo.com/docs/api-endpoints/simplegeo-context)
- [OpenStreetMap API](https://wiki.openstreetmap.org/wiki/API_v0.6#Retrieving_map_data_by_bounding_box:_GET_.2Fapi.2F0.6.2Fmap)

Response
----------------------------
geogeo will create a folder with the county name containing the location specified and download and unzip the following, if available:

- Tiger Census Block Shapefile for 2000 and 2010
- Tiger Census Block Group Shapefile for 2000 and 2010
- Tiger Census Tract Shapefile for 2000 and 2010
- Tiger County Subdivision Shapefile for 2000 and 2010
- Tiger Voting District Shapefile for 2000 and 2010
- Tiger All Lines Shapefile
- Tiger All Roads Shapefile
- Tiger Area Hydrography Shapefile
- Tiger Linear Hydrography Shapefile
- Tiger Area Landmark Shapefile
- Tiger Point Landmark Shapefile
- Tiger Topological Faces (Polygons With All Geocodes) Shapefile
- Tiger Address Range-Feature Name Relationship File Shapefile
- Tiger Address Ranges Relationship File Shapefile
- Feature Names Relationship File Shapefile
- Tiger Topological Faces-Area Hydrography Relationship File Shapefile
- Tiger Topological Faces-Area Landmark Relationship File Shapefile
- OSM Map Data
- SimpleGeo Context API JSON response


Credits
----------------------------

#### Jedidiah Horne jed@blinktag.com
#### Brendan Nee brendan@blinktag.com

License 
----------------------------

(The MIT License)

Copyright (c) 2010 BlinkTag Inc &lt;info@blinktag.com&gt;

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.