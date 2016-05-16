# import all the modules 
import sys
from osgeo import gdal
import matplotlib.pyplot as pyplot
import numpy
gdal.UseExceptions()

# tell poeple how to use the code
def Usage():
    print("""
    $ visualize.py [ band number ] input-file
    """)
    sys.exit(1)
# get the grid data, set nodata value to nan and plot
def main( band_num, input_file ):
    src_ds = gdal.Open( input_file )
    if src_ds is None:
        print 'Unable to open %s' % src_filename
        sys.exit(1)
    try:
        srcband = src_ds.GetRasterBand(band_num)
    except RuntimeError, e:
        print 'No band %i found' % band_num
        print e
        sys.exit(1)

    #print tif.GetMetadata()
    band = src_ds.GetRasterBand(band_num)
    #Nodata = band.GetNoDataValue()
    bandArray = band.ReadAsArray()
    bandArray[bandArray == band.GetNoDataValue()]= numpy.nan
    #print band1Array
   
    imgplot2 = pyplot.imshow(bandArray)
    pyplot.colorbar()
    pyplot.show()

if __name__ == '__main__':

    if len( sys.argv ) < 2:
        print """
        [ ERROR ] you must supply at least two arguments:
        1) the band number to retrieve 
	2) input raster
        Use $ gdalinfo input_file.tif
	to get the information of the Geotiff file
	"""
        Usage()

    main( int(sys.argv[1]), sys.argv[2])
