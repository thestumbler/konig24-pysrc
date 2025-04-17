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
def button_bounding_box( name, size, ctr, rad, rotate=2 ):
  x0 = round( ctr[0] * size )
  y0 = round( ctr[1] * size )
  if rotate == 0:
    x = x0
    y = y0
  if rotate == 2:
    x = round( (1.0-ctr[0]) * size )
    y = round( (1.0-ctr[1]) * size )
  r = round( rad * size )
  xminmax = ( clip((x-r), 0, size), 
              clip((x+r), 0, size) )
  yminmax = ( clip((y-r), 0, size),
              clip((y+r), 0, size) )
  # return f'{name} Button xmin,xmax  ymin,ymax:   ' \
  #        f'{xminmax[0]:4d},{xminmax[1]:4d}   ' \
  #        f'{yminmax[0]:4d},{yminmax[1]:4d}\n' \
  #        f'{name} Button ctr: {x:4d},{y:4d}  rad={r:4d}' 

  # ========================================================================
  # Button bounding boxes for touch screen
  # this information printed by mkface.py script
  # BOTH Button xmin,xmax  ymin,ymax:     91, 149     79, 137
  # Ch1 Button xmin,xmax  ymin,ymax:     24,  72     43,  91
  # Ch2 Button xmin,xmax  ymin,ymax:    168, 216     43,  91
  # LOGO Button xmin,xmax  ymin,ymax:     88, 152      0,  63
  # BOTH Button ctr:  120, 108  rad=  29
  # OUT1 Button ctr:   48,  67  rad=  24
  # OUT2 Button ctr:  192,  67  rad=  24
  # LOGO Button ctr:  120,  32  rad=  32
  return '\n'.join([
    f'self.{name}_GEO = ( {x0:4d}, {y0:4d}, {r:4d} )',
    f'self.{name}_XLIM = ( {xminmax[0]:4d}, {xminmax[1]:4d} )',
    f'self.{name}_YLIM = ( {yminmax[0]:4d}, {yminmax[1]:4d} )',
  ])
  #     self.BOTH_GEO = ( 120, 108, 29 )
  #     self.both_xlim = ( 91, 149 )
  #     self.both_ylim = ( 79, 137 )
  #     self.OUT1_GEO = ( 48,  67 , 24 )
  #     self.ch1_xlim = (  24,  72 )
  #     self.ch1_ylim = (  43,  91 )
  #     self.OUT2_GEO = ( 192,  67, 24 )
  #     self.ch2_xlim = ( 168, 216 )
  #     self.ch2_ylim = (  43,  91 )
  #     self.LOGO_GEO  = (120,  220,  32 )
  #     self.logo_xlim =  ( 88, 152 )
  #     self.logo_ylim = ( 0,  63 )
