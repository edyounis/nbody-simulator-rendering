#!/bin/python
from sys import argv
from PIL import Image
from PIL import ImageDraw

def circle_as_4_tuple ( center, size ):
	return ( center[0]-size, center[1]-size, center[0]+size, center[1]+size )

if len( argv ) < 3:
	print( "Usage is render.py <input file> <output file> [cutoff]" )

input_file  = argv[1]
output_file = argv[2]
cutoff = None if len( argv ) <= 3 else float( argv[3] )

lines = None
with open( input_file, 'r' ) as f:
	lines = f.readlines()

n       = int(   lines[0].split()[0] )
boxsize = float( lines[0].split()[1] )

data = []
# Data is a list a list
# Outer list represents time steps
# Inner list represents all point (x,y)'s in that time step
# There is probabily a better way to do this

for i, line in enumerate( lines[1:] ):
	if len( data ) <= i // n:
		data.append( [] )
	line_split = line.split()
	center_x = int(1024*(float(line_split[0])/boxsize)) # Ugly code
	center_y = int(1024*(float(line_split[1])/boxsize)) # is so hot right now
	data[ i // n ].append( ( center_x, center_y ) ) # https://imgflip.com/s/meme/Mugatu-So-Hot-Right-Now.jpg

frames = []
for data_frame in data:
	img = Image.new( 'L', (1024, 1024), 'white' )
	drawer = ImageDraw.Draw( img )
	for data_point in data_frame:
		if cutoff:
			drawer.ellipse( circle_as_4_tuple( data_point, int(1024*(cutoff / boxsize)) ), 'yellow' )
		drawer.ellipse( circle_as_4_tuple( data_point, 1 ), 'black' )
	frames.append( img )

frames[0].save( output_file, format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0 )
