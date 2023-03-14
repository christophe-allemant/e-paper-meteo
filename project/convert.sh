#!/bin/sh
# convert the picture to the displayable format
# launch : sh convert.sh {name of the file without entension}
# The raw file have a name with _raw at the end
convert pic/$1_raw.bmp -dither FloydSteinberg -remap pic/5in83.bmp  pic/$1.bmp
