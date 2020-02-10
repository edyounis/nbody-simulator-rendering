#!/usr/bin/env python3

from itertools import groupby
from sys import argv, exit

from PIL import Image
from PIL import ImageDraw

# Parse Command Line Arguments
if len( argv ) < 3:
    exit( "Usage is render.py <input file> <output file> [cutoff]" )

input_file = argv[1]
output_file = argv[2]
cutoff = None if len( argv ) <= 3 else float( argv[3] )


# Helper Functions
def circle_to_box ( center_x, center_y, size ):
    return ( center_x - size, center_y - size,
             center_x + size, center_y + size )


# Process the file
with open( input_file, 'r' ) as f:
    # Get first line to find the number of particles and the box size.
    num_parts, box_size = next( f ).split()
    num_parts, box_size = int( num_parts ), float( box_size )

    # Compute cutoff_radius
    cutuff_radius = int( 1024 * ( ( cutoff or 0 ) / box_size ) )

    # Parse input file
    frames = []
    file_sections = groupby( f, lambda x: x and not x.isspace() )
    frame_sections = ( x[1] for x in file_sections if x[0] )

    for frame_section in frame_sections:
        # Set up a new frame
        img = Image.new( 'L', (1024, 1024), 'white' )
        drawer = ImageDraw.Draw( img )
        frames.append( img )

        # Paint in the frame
        for line in frame_section:
            center_x, center_y = line.split()
            center_x = int( 1024 * ( float( center_x ) / box_size ) )
            center_y = int( 1024 * ( float( center_y ) / box_size ) )

            drawer.ellipse( circle_to_box( center_x, center_y, cutuff_radius ),
                            'yellow' )
            drawer.ellipse( circle_to_box( center_x, center_y, 1 ), 'black' )

    frames[0].save( output_file, format='GIF', append_images=frames[1:],
                    save_all=True, duration=100, loop=0 )