#import all the modules 
import sys
from osgeo import gdal
import matplotlib.pyplot as pyplot
import numpy as np
gdal.UseExceptions()
#parameters
Nodata = -3.40282e+38
minvel = 0.0
maxvel = 15.0
deltx = 100.0
delty = 100.0
xl_ori = 687671.375
xr_ori = 730771.375
yu_ori = 8880255.000
yl_ori = 8817855.000
xl = 703000.375
xr = 720000.375
yu = 8850000.000
yl = 8825420.000
date= ('20120419','20120829','20121228','20131112','20140723')
datelabel= ('2012/04/19','2012/08/29','2012/12/28','2013/11/12','2014/07/23')
shapeName='b3_calving_front_'
shapeE='.shp.txt'
shapeDir='/home/ygong/Documents/Acamedia/Projects/ASF/DATANEW/VelocityData_Thomas/b3_calving_front_outline/'
rasterDir='/home/ygong/Documents/Acamedia/Projects/ASF/DATANEW/VelocityData_Thomas/velocity/'
input_raster="".join((rasterDir,'vel_mday_fil_20120419_20120430_300_344_50_57_geo.tif'))
src_ds = gdal.Open( input_raster )
band = src_ds.GetRasterBand(1)
Nodata = band.GetNoDataValue()
bandArray = band.ReadAsArray()
bandArray[bandArray == band.GetNoDataValue()]= np.nan
Vel2D = bandArray[(yu_ori-yu)/delty:(yu_ori-yl)/delty,(xl-xl_ori)/deltx:(xr-xl_ori)/deltx]
##try with the grid data
#load data
ax = pyplot.figure()
imgplot = pyplot.imshow(Vel2D, extent=[xl/1000, xr/1000, yl/1000, yu/1000], vmin=minvel, vmax=maxvel,cmap='gray_r')
for p in range(0, len(date)):
	#print date[p]
	input_shape="".join((shapeDir,shapeName,date[p],shapeE))
	CFArray = np.loadtxt(input_shape)
	pyplot.plot(CFArray[:,0]/1000, CFArray[:,1]/1000, linewidth=3, label=datelabel[p])

pyplot.legend(loc='upper left')
pyplot.axis([xl/1000.0,xr/1000.0,yl/1000.0,yu/1000.0])
pyplot.xlabel('Easting UTM33X (km)', fontsize=15)
pyplot.ylabel('Northing UTM33X (km)', fontsize=15)
pyplot.xticks(fontsize=15)
pyplot.yticks(fontsize=15)
pyplot.grid(b=None, which='major', axis='both')
pyplot.show()
