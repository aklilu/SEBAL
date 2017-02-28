# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 08:12:55 2016
Tim Hessels

To tun this tool PYTROLL/mpop must be installed (http://www.pytroll.org/)

Download the VIIRS input data here: https://www.class.ncdc.noaa.gov/

Change line 21 and 22 to define the input and output files and change the region in line 81 and run the code

"""

import numpy as np
import os
import mpop
from mpop.satellites import PolarFactory
from datetime import datetime

# Define input files and output files
geofile="D:/VIIRS_test/GITCO_npp_d20160224_t1322059_e1327463_b22419_c20160224192747453309_noaa_ops.tif"
outfile='D:/VIIRS_test/VIIRS_SVI05_npp_d20160224_t1322059_e1327463_b22419_c20160224192747453309_noaa_ops.tif'

# Collect general data from the name of the input files
year = np.int((geofile.split(os.sep)[-1]).split('_')[3][1:5])
month = np.int((geofile.split(os.sep)[-1]).split('_')[3][5:7])
day = np.int((geofile.split(os.sep)[-1]).split('_')[3][7:9])
hour = np.int((geofile.split(os.sep)[-1]).split('_')[4][1:3])
minute = np.int((geofile.split(os.sep)[-1]).split('_')[4][3:5])
orbit = (geofile.split(os.sep)[-1]).split('_')[6][1:6]
endHour = np.int((geofile.split(os.sep)[-1]).split('_')[5][1:3])
endMinute = np.int((geofile.split(os.sep)[-1]).split('_')[5][3:5])
start = datetime(year, month, day, hour, minute)
end = datetime(year, month, day, endHour, endMinute)

#geofile is just your GITCO* file
time_slot = datetime(year, month, day, hour, minute)
global_data = PolarFactory.create_scene("npp", "", "viirs", time_slot, orbit)

'''
import utils
import osr
import pyproj
srs = osr.SpatialReference()
srs.ImportFromEPSG(3857)
wgs84 = osr.SpatialReference()
wgs84.ImportFromEPSG(4326)

proj4_args =srs.ExportToProj4()
proj4_args = '%s %s %s %s %s %s %s %s %s' % (proj4_args.split( ' ')[0][1:], \
proj4_args.split( ' ')[1][1:], proj4_args.split( ' ')[2][1:], proj4_args.split( ' ')[3][1:] \
, proj4_args.split( ' ')[4][1:], proj4_args.split( ' ')[5][1:], proj4_args.split( ' ')[6][1:] \
, proj4_args.split( ' ')[7][1:], proj4_args.split( ' ')[8][1:])


latlim = [12,37]
lonlim = [-20,0]

osng = osr.SpatialReference()
osng.ImportFromEPSG(3857)
wgs84 = osr.SpatialReference()
wgs84.ImportFromEPSG(4326)

wgs84=pyproj.Proj("+init=EPSG:4326") # UK Ordnance Survey, 1936 datum


geoProj=pyproj.Proj("+init=EPSG:3857")

ur =pyproj.transform(wgs84, geoProj, lonlim[1],latlim[1])
ll=pyproj.transform(wgs84, geoProj, lonlim[0],latlim[0])
area_extent = (ll[0],ll[1],ur[0],ur[1])
area_id= 'viirs_data'
area_name = 'viirs_data'
proj_id = 'viirs_data'

area_def = utils.get_area_def(area_id, area_name, proj_id, proj4_args,int(6000), int(8000), area_extent)

''' 

from mpop.projector import get_area_def
area_def = get_area_def("Tadla")
global_data.load(['I05'],time_interval=(start,end))
global_data.image.channel_image(11.5).show() #1: 0.64 2: 0.87 3:1.61 4:3.74 5: 11.5
local_data = global_data.project(area_def, mode='nearest')

#pick an area_def I have actually created one based on the extent of VIIRS swath.  That is advanced so just pick one of the built in area_def for where your swath is located to get the hang of it.

loclocal_data = local_data['I05']
img = loclocal_data.as_image(stretched=False)
img.time_slot = time_slot

# you can save the image as a geotiff below#

img.geotiff_save(outfile,compression=0, tags=None, gdal_options=None, blocksize=0, geotransform=None, spatialref=None, floating_point=True)
