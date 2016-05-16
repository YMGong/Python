from osgeo import ogr
from shapely.geometry import Polygon
import sys
import gdal
import numpy as np
#gdal.UseExceptions()

def Usage():
    print("""
    $ creatshape.py input-file
    """)
    sys.exit(1)
    
def main( input_file ):
    data = np.loadtxt( input_file)
    poly = Polygon(data)
    # Here's an example Shapely geometry
    # Now convert it to a shapefile with OGR    
    driver = ogr.GetDriverByName('Esri Shapefile')
    ds = driver.CreateDataSource('test.shp')
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
     
if __name__ == '__main__':

    if len( sys.argv ) < 3:
        print """
        [ ERROR ] you must supply at least two arguments:
        1) the input footprint and 2) output file name with '.shp' suffix
        """
        Usage()

    main( sys.argv[1] )
