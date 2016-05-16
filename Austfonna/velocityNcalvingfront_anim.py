#import all the modules 
import sys
from osgeo import gdal
import matplotlib.pyplot as pyplot
import numpy as np
import os
import matplotlib.animation as animation
import glob
gdal.UseExceptions()

pyplot.rcParams['animation.ffmpeg_path'] = '/usr/share/ffmpeg'
#parameters
band_num = 1

xl = 691671.375
xr = 722000.375
yu = 8857010.000
yl = 8825420.000
#691671.375 728571.375 8871755.0 8823255.0
minvel = 0.0
maxvel = 15.0
dateS='20120419'
dateE='20120430'
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
#input_shape="".join((shapeDir,shapeName,dateE,shapeE))

geo_files = [f for f in os.listdir(rasterDir) if f.endswith('geo.tif')]
geo_files.sort()
#shape_files = [f for f in os.listdir(shapeDir) if f.endswith('shp.txt')]
#shape_files.sort()
#geo_files = glob.glob("".join((rasterDir,'*_geo.tif')))
#geo_files = glob.glob('*_geo.tif')
input_shape="".join((shapeDir,shapeName,dateE,shapeE))
input_raster="".join((rasterDir,rasterName,dateS,'_',dateE,rasterE))
CFArray = np.loadtxt(input_shape)

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

fig = pyplot.figure()
Arrayplot, = pyplot.plot(CFArray[:,0]/1000, CFArray[:,1]/1000,'-k')
imgplot = pyplot.imshow(Vel2D, extent=[xl/1000, xr/1000, yl/1000, yu/1000], vmin=minvel, vmax=maxvel,cmap='jet')
cbar=pyplot.colorbar()	
cbar.set_label(r'Velocity (m day$^{-1}$)', fontsize=15)
cbar.ax.tick_params(labelsize=15)
pyplot.xlabel('Easting UTM33X (km)', fontsize=15)
pyplot.ylabel('Northing UTM33X (km)', fontsize=15)
pyplot.xticks(fontsize=15)
pyplot.yticks(fontsize=15)
pyplot.grid(b=None, which='major', axis='both')
ax = pyplot.gca()
title_obj = ax.text(693,8855,'')
title_obj.set_fontsize(25)
title_obj.set_color('r')
#time_text = ax.text(5, 5,'')
def init():
	title_obj.set_text(" ")
	return imgplot, title_obj
def animate(i):
	#CFArray = np.loadtxt("".join((shapeDir,shape_files[i])))
	input_shape = "".join((shapeDir,shapeName,geo_files[i][22:30],shapeE))
	if os.path.isfile(input_shape):
		print 'calving front:', input_shape
	else:
		input_shape = "".join((shapeDir,shapeName,geo_files[i][13:21],shapeE))
		print 'calving front:', input_shape
	CFArray = np.loadtxt(input_shape)
	src_ds = gdal.Open( "".join((rasterDir,geo_files[i])) )
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
	title_obj.set_text("".join((str(i),':',geo_files[i][13:30])))
	Arrayplot.set_xdata(CFArray[:,0]/1000)
	Arrayplot.set_ydata(CFArray[:,1]/1000)
	#Arrayplot.plot(CFArray[:,0]/1000, CFArray[:,1]/1000,'-k')	
	imgplot.set_array(Vel2D)
	
	#pyplot.setp(title_obj,text="".join((str(i),':',geo_files[i])))    
	print 'velocity:', geo_files[i][13:31]	
	print i,':',xl_ori,xr_ori,yu_ori,yl_ori
	return imgplot, title_obj, Arrayplot

#print band1Array
ani = animation.FuncAnimation(fig, animate, init_func = init, blit=True, frames=27)
ani.save('Basin3SpeedUp.mp4', writer = 'FFwriter', fps=5, extra_args=['-vcodec', 'libx264'])
pyplot.show()

