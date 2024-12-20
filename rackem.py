#!/usr/bin/env python

from dataclasses import dataclass

from pint import UnitRegistry
u = UnitRegistry()

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

@dataclass
class Panel:
  H1U = 1.750 * u.inches
  GAP = 0.03125 * u.inches
  # panel definitions
  n1u: int #number of 1U tall
  def __post_init__( self ):
    # height of defined panel
    self.hgt = self.n1u * Panel.H1U - Panel.GAP
  def __repr__(self):
    return \
      f'{self.n1u}U  ' \
      f'{self.hgt.to(u.inches):10.3f~#P}' \
      f'{self.hgt.to(u.mm):10.2f~#P}'
  def __str__(self):
    return self.__repr__()


