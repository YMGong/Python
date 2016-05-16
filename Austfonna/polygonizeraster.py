from osgeo import gdal, ogr
import sys
# this allows GDAL to throw Python Exceptions
gdal.UseExceptions()

#
#  get raster datasource
#
src_ds = gdal.Open( "vel_utm_mday_fil_20130130_20130210_300_344_50_57_geo.tif" )
if src_ds is None:
    print 'Unable to open %s' % src_filename
    sys.exit(1)

try:
    srcband = src_ds.GetRasterBand(1)
except RuntimeError, e:
    # for example, try GetRasterBand(10)
    print 'Band ( %i ) not found' % band_num
    print e
    sys.exit(1)

#
#  create output datasource
#
dst_layername = "POLYGONIZED_STUFF"
drv = ogr.GetDriverByName("ESRI Shapefile")
dst_ds = drv.CreateDataSource( dst_layername + ".shp" )
#dst_layer = dst_ds.CreateLayer(dst_layername, srs = None )

#gdal.Polygonize( srcband, None, dst_layer, -1, [], callback=None )
