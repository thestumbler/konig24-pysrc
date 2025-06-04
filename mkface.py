#!/usr/bin/env python

#CALIBRATE = True
CALIBRATE = False

DRAW_LOGO = True
#DRAW_LOGO = False

# CONSTRUCTION draws the meter face card with some 
# auxiliary information and lines.
# Turn off CONSTRUCTION for final artwork.
# CONSTRUCTION = True
CONSTRUCTION = False

# MODE selects which meter mode to display 
# on the meter face. 
MODE = 0
VU_MODES = [ 'VU METER', 'LUFS METER', 'PEAK METER' ]


from dataclasses import dataclass
from pathlib import Path
import os
import sys
import random
import math

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.widgets as widgets
from matplotlib.patches import Rectangle, Arc
import matplotlib
# matplotlib.use('tkagg')

from PIL import Image
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import datetime as dt
import vu
from utils import clip, p2r, add2, button_bounding_box


# change matplotlib global settings
plt.rcParams['axes.spines.left'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.bottom'] = False
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.weight'] = 'bold' # you can omit this, it's the default
plt.rcParams['font.sans-serif'] = 'DIN Alternate'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.constrained_layout.use']
# font weights:
#   'normal' 
#   'bold' 
#   'heavy' 
#   'light' 
#   'ultrabold' 
#   'ultralight'

# initialize plot colors
color_mode = 'maroon'
color_hub = 'black'
color_needle_shadow = 'blue'
color_needle = 'black'
color_buttons = 'black'
color_feature = 'green'

# ========================================================================
# Initialilze the plot details
# ========================================================================
my_dpi = 188 # 1.28 in / 240 pixels
img_size = 240 # square image
px = 1/plt.rcParams['figure.dpi']  # pixel in inches
print(px)
fig = plt.figure(figsize=(img_size*px, img_size*px))
#fig = plt.figure(frameon = False)
#fig.set_size_inches(480*px, 480*px)
if MODE == 0:
  fig.set_facecolor( '#ffedb0' ) 
if MODE == 1:
  fig.set_facecolor( 'lavender' ) 
if MODE == 2:
  fig.set_facecolor( 'pink' ) 
print('Background color:',
      matplotlib.colors.to_hex(fig.get_facecolor()) )
# Create an axis that covers the entire figure without any axes
# Note: all coordinates in this code are based on a
# 0,0 to 1,1 square, converted to pixels at the end
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
# Set the limits of the plot
plt.xlim(0, 1)
plt.ylim(0, 1)
# Don't mess with the limits!
plt.autoscale(False)
ax.set_aspect('equal', 'box')
ax.axis('off')

# ========================================================================
# The meter face card consists of these components
# * arc baseline
# * dB scale (tick marks and numbers)
# * linear percent scale (tick marks and numbers)
# * needle
# * needle pivot hub
# * ch1/ch2 mute buttons
# * meter mode label


if CALIBRATE:
  color = 'black'

  circ=plt.Circle(
      (0.5,0.5), radius=0.5, color=color_feature, 
      fill=False,transform=ax.transAxes
  )
  ax.add_patch(circ)

  xc, yc = 0.5, 0.5
  rad = 0.5
  # compass lines, long line points "UP"
  x0, x1 = xc-0.15, xc+0.15
  y0, y1 = yc-0.15, yc+0.25
  ax.plot( [xc, xc], [y0, y1], color=color, linewidth=1 )
  ax.plot( [x0, x1], [yc, yc], color=color, linewidth=1 )

  angles = [ 20, 40, 60 ]
  for a in angles:
    x, y = add2( (xc,yc), p2r(0.10, a) )
    ax.plot( [xc, x], [yc, y], color=color, linewidth=1 )
    ax.text( x,y, str(a), color=color,
      horizontalalignment='left',
      verticalalignment='center',
      fontsize = 8,
      rotation = a, rotation_mode='anchor')

  r45 = 0.9 * rad * math.cos( 45.0 * math.pi / 180.0 )
  labels = [ 
    ( 'SW', ( xc-r45, yc-r45 ) ),
    ( 'NW', ( xc-r45, yc+r45 ) ),
    ( 'NE', ( xc+r45, yc+r45 ) ),
    ( 'SE', ( xc+r45, yc-r45 ) ),
  ]
  for lbl, xy in labels:
    print( lbl, xy )
    ax.text( *xy, lbl, color=color,
      horizontalalignment='center',
      verticalalignment='center',
      rotation = 0, rotation_mode='anchor')
  plt.show(block=False)
  fname = f'calibrate.jpg'
  plt.savefig(fname)
  plt.show()
  sys.exit()




# ========================================================================
# Make the baseline arc for meter scale
# ------------------------------------------------------------------------
# awkward because matpotlib arcs are drawn CCW.
# Also, arcs cannot use endcap BUTT style,
# needed for adjoining the black and red segments.
# Instead , draw arc by many short linear segments
# ========================================================================
aspan = 75           # angular span of meter arc
center = (0.5, 0.1)  # center point of arc
radius = 0.65        # radius of arc
face = vu.Meter(aspan) #degrees

rticklen =  0.05 * radius    # major tick mark length
rticklen2 = 0.65 * rticklen  # minor tick mark length
rtextoff = 1.130 * rticklen    # offset of label text

NSEGS = 200
aref = 90 + 0.5*face.ASPAN
adel = face.ASPAN / float(NSEGS)
x0, y0 = add2( center, p2r( radius, aref ) )
for n in range(1,NSEGS+1):
  a0 = n*adel
  a = aref - a0
  if a0 > face.AZERO: color='red'
  else: color = 'black'
  x1, y1 = add2( center, p2r( radius, a ) )
  ax.plot( [x0, x1], [y0, y1], color=color,
          linewidth=3, solid_capstyle='butt')
  x0,y0 = x1,y1

# ========================================================================
# plot linear percentage scale
# ------------------------------------------------------------------------
if True:
  points = []
  for v100 in face.v100_list:
    points.append( vu.Point(face).from_v100(v100, label=True) )
  for v100 in face.v100_list2:
    points.append( vu.Point(face).from_v100(v100, label=False) )
  points.sort()
  #print("v100 points")
  #for p in points: print(p)
  
  alist = [ p.xangle for p in points ]
  labels = [ p.v100_label for p in points ]
  for a0, label in zip(alist, labels):
    a = 90 + 0.5*face.ASPAN - a0
    # color is always black for linear percentages
    # because these stop at 100% and don't go into the red
    color = 'black'
    if label == '': r100 = radius - rticklen2
    else:           r100 = radius - rticklen
    # convert to x,y values  
    x0, y0 = add2( center, p2r( radius,   a ) )
    x1, y1 = add2( center, p2r( r100, a ) )
    x2, y2 = add2( center, p2r( radius - 1.2*rtextoff, a ) )
    # plot tick mark,
    ax.plot( [x0, x1], [y0, y1], color=color, linewidth=1 )
    # and text
    ax.text(x2, y2, label, color=color,
      horizontalalignment='center',
      verticalalignment='top',
      rotation = 270+a, rotation_mode='anchor')

# ========================================================================
# plot dB scale
# ------------------------------------------------------------------------
if True:
  points = []
  for vdb in face.vdb_list:
    points.append( vu.Point(face).from_vdb(vdb, label=True) )
  for vdb in face.vdb_list2:
    points.append( vu.Point(face).from_vdb(vdb, label=False) )
  points.sort()
  #print("vdb points")
  #for p in points: print(p)
  alist = [ p.xangle for p in points ]
  labels = [ p.vdb_label for p in points ]
  for a0, label in zip(alist, labels):
    a = 90 + 0.5*face.ASPAN - a0
    if a0 > face.AZERO: color = 'red'
    else:               color = 'black'
    if label == '': rdb = radius + rticklen2
    else:           rdb = radius + rticklen
    # convert to x,y values  
    x0, y0 = add2( center, p2r( radius,   a ) )
    x1, y1 = add2( center, p2r( rdb, a ) )
    x2, y2 = add2( center, p2r( radius + rtextoff, a ) )
    # plot tick mark,
    ax.plot( [x0, x1], [y0, y1], color=color, linewidth=1 )
    # and text
    ax.text(x2, y2, label, color=color,
      horizontalalignment='center',
      verticalalignment='bottom',
      rotation = 270+a, rotation_mode='anchor')


# ========================================================================
# plot needle range and sample needle
# ------------------------------------------------------------------------
rad_needle_beg = 0.25 * radius
rad_needle_tip = 0.98 * radius 
if CONSTRUCTION:
  # draw a meter needle range (min/max)
  a = 90 + 0.5*face.ASPAN
  x0, y0 = add2( center, p2r( rad_needle_beg, a ) )
  x1, y1 = add2( center, p2r( rad_needle_tip, a ) )
  ax.plot( [x0, x1], [y0, y1], color=color_needle_shadow, 
          linestyle='dashed', linewidth=0.5 )
  a = 90 - 0.5*face.ASPAN
  x0, y0 = add2( center, p2r( rad_needle_beg, a ) )
  x1, y1 = add2( center, p2r( rad_needle_tip, a ) )
  ax.plot( [x0, x1], [y0, y1], color=color_needle_shadow, 
          linestyle='dashed', linewidth=0.5 )
  # and draw an example needle
  ang_needle = 0.33 * face.ASPAN
  a = 90 + 0.5*face.ASPAN - ang_needle
  x0, y0 = add2( center, p2r( rad_needle_beg, a ) )
  x1, y1 = add2( center, p2r( rad_needle_tip, a ) )
  #ax.plot( [x0, x1], [y0, y1], color=color_needle, 
  #        linestyle='solid', linewidth=1 )
  ax.arrow( x0, y0, (x1-x0), (y1-y0),  head_width=0.015, 
           head_length=0.075, linewidth=0.5, color=color_needle,
           length_includes_head=True)


# ========================================================================
# plot needle pivot center mark 
# ------------------------------------------------------------------------
if False:
  mark = 0.1 * radius
  x0, y0 = add2( center, ( -mark, 0 ) )
  x1, y1 = add2( center, ( +mark, 0 ) )
  ax.plot( [x0, x1], [y0, y1], color=color_feature, linewidth=1 )
  x0, y0 = add2( center, ( 0, -mark ) )
  x1, y1 = add2( center, ( 0, +mark ) )
  ax.plot( [x0, x1], [y0, y1], color=color_feature, linewidth=1 )

# ========================================================================
# plot cicle around the edge of the LCD, which is circular, not square
# ------------------------------------------------------------------------
# if CONSTRUCTION:
if True:
  circ=plt.Circle(
      (0.5,0.5), radius=0.5, color=color_feature, 
      fill=False,transform=ax.transAxes
  )
  ax.add_patch(circ)

# ========================================================================
# plot the meter mode text 
# ------------------------------------------------------------------------
if True:
  str_mode = VU_MODES[MODE]
  xylogo = ( 0.5, 0.93 )
  ax.text( *xylogo, str_mode, color=color_mode, 
    fontsize = 12,
    horizontalalignment='center',
    verticalalignment='top')

# ========================================================================
# plot the meter hub
# ------------------------------------------------------------------------
if True:
  NSEGS = 100
  #aref = 90 + 0.5*face.ASPAN
  #adel = face.ASPAN / float(NSEGS)
  aref = 180.0
  adel = 180.0 / float(NSEGS)
  x0, y0 = add2( center, p2r( rad_needle_beg, aref ) )
  for n in range(1,NSEGS+1):
    a0 = n*adel
    a = aref - a0
    x1, y1 = add2( center, p2r( rad_needle_beg, a ) )
    ax.plot( [x0, x1], [y0, y1], color=color_hub,
            linewidth=2, solid_capstyle='butt')
    x0,y0 = x1,y1
  yedge = math.sqrt( 0.5**2 - rad_needle_beg**2 )
  yintersect = 0.5 - yedge
  x0, y0 = center[0]-rad_needle_beg, center[1]
  x1, y1 = center[0]-rad_needle_beg, yintersect
  ax.plot( [x0, x1], [y0, y1], color=color_hub,
          linewidth=2, solid_capstyle='butt')
  x0, y0 = center[0]+rad_needle_beg, center[1]
  x1, y1 = center[0]+rad_needle_beg, yintersect
  ax.plot( [x0, x1], [y0, y1], color=color_hub,
          linewidth=2, solid_capstyle='butt')

# ========================================================================
# plot logo image inside the meter hub
# ------------------------------------------------------------------------
# Load logo image
xylogo_fudge = (0.01, -0.015)
xylogo_base = (0.5,  0.5*(center[1]+rad_needle_beg))
xylogo = tuple(p+q for p, q in zip(xylogo_base, xylogo_fudge))

b3rad = xylogo[1]
bbox3 = button_bounding_box( 'LOGO', img_size, xylogo, b3rad )
if DRAW_LOGO:
  #zoom = 0.08
  #w, h = 466, 466
  #image_path = "logos/two-way-transparent.png"
  zoom = 0.20
  w, h = 240, 240
  #image_path = "logos/logo-intraframe-240px.png"
  image_path = "logos/intraframe-square-combined.png"
  image_data = Image.open(image_path).convert('RGBA')
  zoom_factor = min(w / image_data.width, h / image_data.height) * zoom
  image_box = OffsetImage(image_data, zoom=zoom_factor)
  anno_box = AnnotationBbox(image_box, 
                            xy=xylogo, xycoords='axes fraction', 
                            box_alignment=(0.5, 0.5), frameon=False)
  ax.add_artist(anno_box)

# ========================================================================
# plot circle representing the button area, demo feature
# ------------------------------------------------------------------------
if CONSTRUCTION:
  circ=plt.Circle( xylogo, radius = b3rad, 
      linewidth=1, fill=False, color=color_feature,
      transform=ax.transAxes
  )
  ax.add_patch(circ)

# ========================================================================
# plot two audio mute buttons, ch1 and ch2
# ------------------------------------------------------------------------
# drawing the buttons consists of three steps:
# * draw the filled colored circle
# * draw border around the circle
# * draw the button text
xych0 = ( 0.50, 0.45 ) #hidden mute all
xych1 = ( 0.20, 0.28 )
xych2 = ( 0.80, 0.28 )
rad_mute = 0.10
# Prepare the button bounding boxes for touchscreen
bbox0 = button_bounding_box( 'ALL', img_size, xych0, 1.2*rad_mute )
bbox1 = button_bounding_box( 'CH1', img_size, xych1, rad_mute )
bbox2 = button_bounding_box( 'CH2', img_size, xych2, rad_mute )
if CONSTRUCTION:
  # draw hidden button circle for mute all
  circ=plt.Circle( xych0, radius = 1.2*rad_mute, 
      linewidth=1, fill=False, color=color_feature,
      transform=ax.transAxes
  )
  ax.add_patch(circ)
if CONSTRUCTION:
  # CHANNEL 1 BUTTON
  circ=plt.Circle( xych1, radius = rad_mute, 
      linewidth=1, fill=True, color='yellowgreen', 
      transform=ax.transAxes
  )
  ax.add_patch(circ)
if True:
  circ=plt.Circle( xych1, radius = rad_mute, 
      linewidth=3, fill=False, color=color_buttons,
      transform=ax.transAxes
  )
  ax.add_patch(circ)
  rad_off_label = 0.9*rad_mute
  xyanchor = add2( xych1, [-rad_off_label, rad_off_label] )
  ax.text( *xyanchor, 'OUT1', color=color_buttons, 
    fontsize = 14, fontweight = 'bold',
    horizontalalignment='right',
    verticalalignment='bottom',
    rotation = 270.0+0.5*face.ASPAN, rotation_mode='anchor')
  # CHANNEL 2 BUTTON
if CONSTRUCTION:
  circ=plt.Circle( xych2, radius = rad_mute, 
      linewidth=1, fill=True, color='tomato', 
      transform=ax.transAxes
  )
  ax.add_patch(circ)
if True:
  circ=plt.Circle( xych2, radius = rad_mute, 
      linewidth=3, fill=False, color=color_buttons,
      transform=ax.transAxes
  )
  ax.add_patch(circ)
  xyanchor = add2( xych2, [rad_off_label, rad_off_label] )
  ax.text( *xyanchor, 'OUT2', color=color_buttons, 
    fontsize = 14, fontweight = 'bold',
    horizontalalignment='left',
    verticalalignment='bottom',
    rotation = 90.0-0.5*face.ASPAN, rotation_mode='anchor')

# Print the button bounding boxes for touchscreen
print(bbox0)
print(bbox1)
print(bbox2)
print(bbox3)


#fig.patch.set_visible(False)
#plt.tight_layout()
#plt.show()
plt.show(block=False)
fname = f'face{MODE:1d}.jpg'
plt.savefig(fname)
#plt.savefig("face.jpg")
plt.show()

