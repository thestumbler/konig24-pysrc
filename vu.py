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
  def __init__(self, aspan):
    self.ASPAN = aspan  # meter span, delta degrees
    self.VDBMAX = 3.0    # max dB span
    self.VDBMIN = -20.0  # min dB span (not realy minimum of meter)
    self.V100FS = 100 * 10.0 ** (self.VDBMAX / 20.0) # full scale in V100 percent
    self.XZERO = 100.0 / self.V100FS  # 0 db / 100 pct point as fraction of span
    self.AZERO = self.ASPAN * self.XZERO
    # main lists have labels, secondary lists just tick marks
    self.v100_list = [ x for x in range(20, 101, 20) ]
    self.v100_list2 = [0] + [ x for x in range(10, 100, 20) ]
    self.vdb_list = [ -100, -20, -10, -7, -5, -3, -2, -1, 0, 1, 2, 3 ]
    self.vdb_list2 = [ -6, -4, -0.5, 0.5 ]

  def __repl__(self):
    return \
      f'ASPAN   {self.ASPAN:10f }  meter span, delta degrees\n' \
      f'VDBMAX  {self.VDBMAX:10f}  max dB span\n' \
      f'VDBMIN  {self.VDBMIN:10f}  min dB span (not realy minimum of meter)\n' \
      f'V100FS  {self.V100FS:10f}  full scale in V100 percent\n' \
      f'XZERO   {self.XZERO:10f }  0 db / 100 pct point as fraction of span\n'

  def __str__(self):
    return self.__repr__()

class Point:
  INFINITY = r'-$\infty$  '
  xfrac: float  # meter span, fraction (0.0 to 1.0)
  xangle: float # meter span, angle
  v100: float   # voltage, percentage
  vdb:  float   # voltage, dB
  v100_label: str
  vdb_label: str
  def __init__(self, meter):
    self.meter = meter

  def __lt__(a, b):
    return a.xfrac < b.xfrac

  def __eq__(self, other):
    return a.xfrac == b.xfrac

  def make_label(self, label):
    self.label = label
    self.v100_label = ''
    self.vdb_label = ''
    if self.label:
      self.v100_label =  f'{self.v100}'
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

  def from_v100(self, _v, label=False):
    self.v100 = clip( _v, 0.0, self.meter.V100FS )
    self.xfrac = self.v100 / self.meter.V100FS
    self.xangle = self.xfrac * self.meter.ASPAN
    if(self.v100 <= 0.0): self.vdb = float('nan')
    else: self.vdb = 20.0 * math.log10(self.v100/100.0)
    self.make_label(label)
    return self

  def from_vdb(self, _d, label=False):
    # -100 dB or below to be infinity
    if _d <= -100:
      self.vdb = float('nan')
      self.v100 = 0.0
    else:
      self.vdb = clip( _d, -100.0, +3.0 )
      self.v100 = 100.0 * 10.0 ** (self.vdb / 20.0)
    self.xfrac = self.v100 / self.meter.V100FS
    self.xangle = self.xfrac * self.meter.ASPAN
    self.make_label(label)
    return self

  def __repr__(self):
    return \
        f'{self.xfrac:10.4f} frac' \
        f'{self.xangle:10.2f} degs' \
        f'{self.v100:10.2f} %' \
        f'{self.vdb:10.2f} dB' \
        f'{self.label:2d}' \
        f'{self.v100_label:>8s}' \
        f'{self.vdb_label:>8s}'

  def __str__(self):
    return self.__repr__()

