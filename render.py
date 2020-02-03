#!/bin/python
from sys import argv
from PIL import Image
from PIL import ImageDraw

# Parse Command Line Arguments
if len( argv ) < 3:
    print( "Usage is render.py <input file> <output file> [cutoff]" )

input_file  = argv[1]
output_file = argv[2]
cutoff = None if len( argv ) <= 3 else float( argv[3] )


# Helper Functions
def circle_as_4_tuple ( center, size ):
    return ( center[0]-size, center[1]-size, center[0]+size, center[1]+size )


lines = None
with open( input_file, 'r' ) as f:
    lines = f.readlines()

num_parts = int(   lines[0].split()[0] )
boxsize   = float( lines[0].split()[1] )

data = [ [] ]
# Data is a list of lists
# Outer list represents time steps
# Inner list represents all point (x,y)'s in that time step
# There is probably a better way to do this

# Parse input file
for line in lines[1:]:

    if line.isspace():
        data.append( [] )
        continue

    line_split = line.split()
    center_x = int( 1024 * ( float( line_split[0] ) / boxsize ) )
    center_y = int( 1024 * ( float( line_split[1] ) / boxsize ) )
    data[ -1 ].append( ( center_x, center_y ) )

# Remove trailing spaces
while len( data[-1] ) == 0:
    data = data[:-1]

# Render GIF
frames = []
for data_frame in data:
    img = Image.new( 'L', (1024, 1024), 'white' )
    drawer = ImageDraw.Draw( img )
    for data_point in data_frame:
        if cutoff:
            drawer.ellipse( circle_as_4_tuple( data_point, int(1024*(cutoff / boxsize)) ), 'yellow' )
        drawer.ellipse( circle_as_4_tuple( data_point, 1 ), 'black' )
    frames.append( img )

# Save output
frames[0].save( output_file, format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0 )
