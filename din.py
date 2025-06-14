#!/usr/bin/env python

import math

from utils import clip, p2r, add2

# VU Meter
#
# 0 to 100 percent spans from 0 to 71% of the scale extent
# dB are plotted from -20 to +3 dB
#
# 0 to 100 VU linear percent spans
# 0 to 71 percent full meter scale

class Meter:
  # define a linear meter baseline spanning 0.0 to 1.0
  # define a arc baseline which spans ASPAN degrees
  def __init__(self, aspan, mode=None, name='METER', color='ivory' ):
    self.mode = mode
    self.name = name
    self.color = color
    self.ASPAN = aspan  # meter span, delta degrees

    # Parameters for the DIN meter scale
    self.k = 1.4  # Compression parameter
    self.p = 2.3  # Power factor

    self.VDBMAX = 5.0    # max dB span
    self.VDBMIN = -50.0  # min dB span (not realy minimum of meter)
    # main lists have labels, secondary lists just tick marks
    self.v100_list = []
    self.v100_list2 = []
    self.vdb_list = [-50, -30, -20, -10, -5, 0, 5]
    self.vdb_list2 = [ -40, -25, 
                      -19, -18, -17, -16, -15, -14, -13, -12, -11, 
                      -9, -8, -7, -6,
                      -4, -3, -2, -1, 
                      1, 2, 3, 4 ]

    self.XZERO = Point(self).from_vdb(0).xfrac
    self.AZERO = self.ASPAN * self.XZERO

  def __repl__(self):
    return \
      f'ASPAN   {self.ASPAN:10f }  meter span, delta degrees\n' \
      f'VDBMAX  {self.VDBMAX:10f}  max dB span\n' \
      f'VDBMIN  {self.VDBMIN:10f}  min dB span (not realy minimum of meter)\n' \

  def __str__(self):
    return self.__repr__()

class Point:
  INFINITY = r'-$\infty$  '
  xfrac: float  # meter span, fraction (0.0 to 1.0)
  xangle: float # meter span, angle
  vdb:  float   # voltage, dB
  vdb_label: str
  def __init__(self, meter):
    self.meter = meter

  def __lt__(a, b):
    return a.xfrac < b.xfrac

  def __eq__(self, other):
    return a.xfrac == b.xfrac

  def make_label(self, label):
    self.label = label
    self.vdb_label = ''
    if self.label:
      if not math.isnan( self.vdb ):
        self.vdb_label = f'{self.vdb}'
      else:
        self.vdb_label = self.INFINITY

  def from_xfrac(self, _x, label=False):
    self.xfrac = clip( _x, 0.0, 1.0 )
    self.xangle = self.xfrac*self.meter.ASPAN
    self.v100 = 100.0 * self.xfrac / self.meter.XZERO 
    if(self.v100 <= 0.0): 
      self.vdb = float('nan')
    else: self.vdb = 20.0 * math.log10(self.v100/100.0)
    self.make_label(label)
    return self

  def from_xangle(self, _a, label=False):
    self.xangle = clip( _a, 0.0, self.meter.ASPAN )
    self.xfrac = self.xangle / self.meter.ASPAN
    self.v100 = 100.0 * self.xfrac / self.meter.XZERO
    if(self.v100 <= 0.0): self.vdb = float('nan')
    else: self.vdb = 20.0 * math.log10(self.v100/100.0)
    self.make_label(label)
    return self

  def from_vdb(self, _d, label=False):
    if _d <= -100:
      # -100 dB or below to be infinity
      self.vdb = float('nan')
      self.xfrac = 0.0
      self.xangle = 0.0
    else:
      # Normalize dB range
      normalized = (_d - min(self.meter.vdb_list) ) \
                 / ( max(self.meter.vdb_list) - min(self.meter.vdb_list) ) 
      # Apply compression formula
      # this returns 
      self.xfrac = \
            ( 1 - math.exp(-self.meter.k * normalized**self.meter.p) ) \
          / ( 1 - math.exp(-self.meter.k) )  
      self.vdb = _d
      self.xangle = self.xfrac * self.meter.ASPAN
      if self.xfrac > 1.0:
        print(f'oops: {_d}')
    self.make_label(label)
    return self

  def __repr__(self):
    return \
        f'{self.xfrac:10.4f} frac' \
        f'{self.xangle:10.2f} degs' \
        f'{self.vdb:10.2f} dB' \
        f'{self.label:2d}' \
        f'{self.vdb_label:>8s}'

  def __str__(self):
    return self.__repr__()

