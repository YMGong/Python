from osgeo import ogr
from shapely.geometry import Polygon
import sys
import gdal
import numpy as np
#gdal.UseExceptions()
#input_file = 'footprint.txt'
#data = np.loadtxt( input_file)
#poly = Polygon(data)
poly = Polygon([(0, 0), (0, 1), (1, 1), (0, 0)])
    # Here's an example Shapely geometry
    # Now convert it to a shapefile with OGR    
driver = ogr.GetDriverByName('ESRI Shapefile')
ds = driver.CreateDataSource('home/ygong/Documents/Acamedia/Projects/ASF/DATANEW/VelocityData_Thomas/b3_calving_front_outline/test.shp')
layer = ds.CreateLayer('', None, ogr.wkbPolygon)
    # Add one attribute
layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
defn = layer.GetLayerDefn()

    ## If there are multiple geometries, put the "for" loop here

    # Create a new feature (attribute and geometry)
feat = ogr.Feature(defn)
feat.SetField('id', 123)

    # Make a geometry, from Shapely object
geom = ogr.CreateGeometryFromWkb(poly.wkb)
feat.SetGeometry(geom)

layer.CreateFeature(feat)
feat = geom = None  # destroy these

    # Save and close everything
ds = layer = feat = geom = None
