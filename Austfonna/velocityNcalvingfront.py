#import all the modules 
import sys
from osgeo import gdal
import matplotlib.pyplot as pyplot
import numpy as np
gdal.UseExceptions()
#parameters
band_num = 1

xl = 691371.375
xr = 722000.375
yu = 8857010.000
yl = 8825420.000

minvel = 0.0
maxvel = 15.0
dateS='20140712'
dateE='20140723'
rasterE='_300_344_50_57_geo.tif'
rasterName='vel_mday_fil_'
rasterDir='/home/ygong/Documents/Acamedia/Projects/ASF/DATANEW/VelocityData_Thomas/velocity/'
shapeName='b3_calving_front_'
shapeE='.shp.txt'
shapeDir='/home/ygong/Documents/Acamedia/Projects/ASF/DATANEW/VelocityData_Thomas/b3_calving_front_outline/'
saveDir='/home/ygong/Documents/Acamedia/Projects/ASF/DATANEW/VelocityData_Thomas/velocity/'
saveName='vel_mday_'
##try with the grid data
#load data
#input_raster='vel_utm_mday_fil_20120419_20120430_300_344_50_57_geo.tif'
input_raster="".join((rasterDir,rasterName,dateS,'_',dateE,rasterE))
input_shape="".join((shapeDir,shapeName,dateE,shapeE))
print 'input raster: ',input_raster
print 'input shape: ',input_shape
src_ds = gdal.Open( input_raster )
band = src_ds.GetRasterBand(band_num)
Nodata = band.GetNoDataValue()
bandArray = band.ReadAsArray()
bandArray[bandArray == band.GetNoDataValue()]= np.nan
gt = src_ds.GetGeoTransform()
x = 0.0 #something to do with the limits
y = 0.0
xl_ori = gt[0] + (x+0.5) * gt[1] + (y+0.5) * gt[2]
xr_ori = xl_ori + gt[1]*(src_ds.RasterXSize-1)
yu_ori = gt[3] + (x+0.5) * gt[4] + (y+0.5) * gt[5]
yl_ori = yu_ori + gt[5]*(src_ds.RasterYSize-1)

Vel2D = bandArray[(yu_ori-yu)/abs(gt[5]):(yu_ori-yl)/abs(gt[5]),(xl-xl_ori)/abs(gt[1]):(xr-xl_ori)/abs(gt[1])]
###
#print band1Array

CFArray = np.loadtxt(input_shape)
fig = pyplot.figure()
pyplot.plot(CFArray[:,0]/1000, CFArray[:,1]/1000,'-k')
imgplot = pyplot.imshow(Vel2D, extent=[xl/1000, xr/1000, yl/1000, yu/1000], vmin=minvel, vmax=maxvel,cmap='jet')
#imgplot2 = pyplot.imshow(bandArray, extent=[xl, xr, yl, yu])
cbar=pyplot.colorbar()
cbar.set_label(r'Velocity (m day$^{-1}$)', fontsize=15)
cbar.ax.tick_params(labelsize=15)
pyplot.xlabel('Easting UTM33X (km)', fontsize=15)
pyplot.ylabel('Northing UTM33X (km)', fontsize=15)
pyplot.xticks(fontsize=15)
pyplot.yticks(fontsize=15)
pyplot.grid(b=None, which='major', axis='both')
fig.savefig("".join((saveDir,saveName,dateS,'_',dateE,'.tif')))
pyplot.show()

