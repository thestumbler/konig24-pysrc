#!/usr/bin/env python

import math

def clip( x, xmin, xmax ):
  if x < xmin: return xmin
  if x > xmax: return xmax
  return x

def p2r( r, adeg ):
  arad = adeg * math.pi / 180.0
  x = r * math.cos(arad)
  y = r * math.sin(arad)
  return x, y

def add2( p1, p2 ):
  return p1[0]+p2[0], p1[1]+p2[1]

# Print the button bounding boxes for touchscreen
# name of button
# size of img in pixels, for scaling
# ctr = (x,y) of button in 0,0,1,1 system
# rad = radius of button
def button_bounding_box( name, size, ctr, rad ):
  x = round( ctr[0] * size )
  y = round( ctr[1] * size )
  r = round( rad * size )
  xminmax = ( clip((x-r), 0, size), 
              clip((x+r), 0, size) )
  yminmax = ( clip((y-r), 0, size),
              clip((y+r), 0, size) )
  return f'{name} Button xmin,xmax  ymin,ymax:   ' \
         f'{xminmax[0]:4d},{xminmax[1]:4d}   ' \
         f'{yminmax[0]:4d},{yminmax[1]:4d}\n' \
         f'{name} Button ctr: {x:4d},{y:4d}  rad={r:4d}' 
