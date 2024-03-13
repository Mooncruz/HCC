#!/bin/bash

#inputs:
input_filename='simu.gro'  # Cytochrome C
#input_filename='3rgk.pdb'  # Myoglobin
#input_filename='193l.pdb'  # Lysozyme C


##############################################################
# define TCL commands in a temporary file:
cat <<EOF > vmd_commands.tcl

# load molecule:
mol new $input_filename


# delete default representation:
mol delrep 0 top


# representation:
mol selection {name L0}
mol representation Lines 6 6	#puede ser=Dotted, VDW, Beads
mol color ColorID 0
mol material Glass1		#puede ser= Transparent, Opaque,Glass1 
mol addrep top


# representation:
mol selection {name L1}
mol representation Lines 6 6	#puede ser=Dotted, VDW, Beads
mol color ColorID 0
mol material Glass1		#puede ser= Transparent, Opaque,Glass1 
mol addrep top


# representation:
mol selection {name L4}
mol representation Lines 6 6	#puede ser=Dotted, VDW, Beads
mol color ColorID 0
mol material Glass1		#puede ser= Transparent, Opaque,Glass1 
mol addrep top


# representation:
mol selection {name L6}
mol representation VDW 6 12	#mol representation Dotted 2 12
mol color ColorID 1
mol material Opaque		#puede ser= Transparent, Opaque,Glass1 
mol addrep top


# general display:
display depthcue off
#display projection orthographic
display shadows on
display ambientocclusion on
axes location off
#axes location lower left
#color Display Background white
#pbc box
display rendermode Normal
display aoambient 0.75
display aodirect 0.75

# rotate:
# first orientation
#rotate x by 32
#rotate y by 0
#rotate z by 0

# second orientation, similar to povray
rotate x by 0
rotate y by 0
rotate z by 0


# camera distance:
scale by 1.2

# set background to transparent:
# sbackground {rgbt <0,0,0,0>}

# render:
render POV3 image.pov povray +W%w +H%h -I%s -O%s.png +X +A +FT +UA
EOF

# add the 'exit' command outside the VMD commands block:
echo "exit" >> vmd_commands.tcl

# execute VMD with the commands defined in the temporary file:
vmd -e vmd_commands.tcl

# delete the temporary file:
rm vmd_commands.tcl

# convert figure to png:
convert image.pov.png.tga image.png

# delete unnecessary files:
\rm image.pov.png.tga
\rm image.pov

# trim figure:
convert -trim image.png image.png 

