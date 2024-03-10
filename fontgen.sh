#!/bin/bash

w=64
h=64
yp=32
xp=32
letter=!
noise=40
output_dir=data/testing


python3 font_generator.py --width $w --height $h --x_position $xp --y_position \
 $yp --letter $letter --noise_level $noise --output_dir $output_dir --overwrite
