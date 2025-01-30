#!/usr/bin/env python

from fractions import Fraction
from dataclasses import dataclass

from pint import UnitRegistry
ureg = UnitRegistry()

# measurements seem to be defined in inches
# oritinally.
#
# * 1U definition:
#   * 1-3/4 in, 1.750 in, 44.45 mm
# * panel shoule be 1/32 in / 0.794 mm smaller, 
#   therefore 1U panel height:
#   * 1-23/32 in, 1.71875 in, 43.66 mm
# 
# The gap allows a bit of room above and below an installed 
# piece of equipment so it may be removed without binding on 
# the adjacent equipment.
# 
# Panel Width
# 
# 19-inch rack hole spacing, center to center
# * 18-5⁄16 in, 18.3125 in, 465.1 mm
# 
# Hammond Mfg
# * w =  `19.00 in   483 mm`
# * h =  ` 1.72 in    44 mm`
# 
# holes details
# * v spacing =  `1.25 in    32 mm`
# * diameter  =  `hole or slot, 0.250 in dia`
# 
# enclosure on panel 
#* i.e., envelope free for mounting
#  equipment to the panel without
#  interfering with the rails.
#* width 16.600 in   421.65 mm, centered
# 
# panel height formula
# 
#   * n = height of panel in 1U units
#   * h = height of panel in inches/mm
#   * formuae:
#   * `  h =  1.75 * n − 0.031   (inches)`
#   * `  h = 44.45 * n − 0.794       (mm)`

#print( f'{x_in:10.3f~#P}{x_mm:10.2f~#P}')

class Fractional_inches:
  def __init__(self, _value):
    self.value = _value
    self.whole = float(int(_value))
    self.fract = Fraction( _value - self.whole )
    if self.fract == 0: self.sfract = '     '
    else: self.sfract = f'-{str(self.fract):<4s}'
  def __repr__(self):
    return f'{self.whole:>2.0f}{self.sfract}'

class Panel:
  H1U = 1.750 * ureg.inches
  GAP = 0.03125 * ureg.inches
  # panel definitions
  def __init__( self, _n1u ):
    self.n1u = _n1u
    # height of defined panel
    self.hgt_panel = self.n1u * Panel.H1U - Panel.GAP
    self.hgt = self.n1u * Panel.H1U
    self.fhgt = Fractional_inches(self.hgt.magnitude)
  def __repr__(self):
    return \
      f'{self.n1u}U  ' \
      f'{self.fhgt}' \
      f'{self.hgt.to(ureg.inch):10.3f~#P}' \
      f'{self.hgt.to(ureg.mm):10.2f~#P}'
  def __str__(self):
    return self.__repr__()


# this doesn't work?
# int has no attribute "inches"
# but works from interactive.
for u in range(1,6):
  p = Panel(u)
  print(p)

