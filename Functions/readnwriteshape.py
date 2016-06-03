#!/usr/bin/env python
###############################################################################
# $Id$
#
# Project:  GDAL
# Purpose:  Script to translate GDAL supported phase into XYZ ASCII
#           point stream.
# Author:   Yongmei Gong
#
###############################################################################

try:
    import shapefile
except ImportError:
    import shapefile

import sys

try:
    import numpy as np
except ImportError:
    import np

# =============================================================================
def Usage():
    print('Usage: shape2xyz.py [-shape number] file')
    print('')
    sys.exit( 1 )

# =============================================================================
#
# Program mainline.
#
def main( shape_num, input_file ):
#read the file
	sf = shapefile.Reader(input_file)
	shapes = sf.shapes()
#read the bounding box from the shape
	bbox = shapes[shape_num].bbox
#get the length of the shape file
	length = len(shapes[shape_num].points)
	array = shapes[shape_num].points[0]
#read the point out in 1 array
	for i in range( 1, length-1 ):
		array = np.append(array, shapes[0].points[i])
		arraynew = np.reshape(array, (len(array)/2, 2))
	print arraynew
if __name__ == '__main__':
	if len( sys.argv ) < 3:
        	print """
        	[ ERROR ] you must supply at least two arguments:
        	1) the shape number to retrieve (starting from 0) and 2) input shape file
        	Use 
		"""
        	Usage()

    	main( int(sys.argv[1]), sys.argv[2] )
















