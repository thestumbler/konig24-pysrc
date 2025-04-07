#!/usr/bin/env python

#@ picotool info | grep "at bus" > out_picotool.txt
#@ lsusb | grep "RP" | grep Boot > out_lsudb.txt
#@ df -lH | grep "/Volumes/RP" > out_diskfree.txt


# this data was figured out manually
# export ad00='/dev/cu.usbmodem11122401'  # proto_digital_00   7DF06CFA89A6F59A   22
# export ad01='/dev/cu.usbmodem11123101'  # proto_digital_01   0C4941E2ADE834E3   39
# export ad02='/dev/cu.usbmodem11123201'  # proto_digital_02   DFB05B2382FFB81D   19
# export ad03='/dev/cu.usbmodem11123301'  # proto_digital_03   9349325338EF36FE   21

serno_to_board_id = {
    0x7DF06CFA89A6F59A : 0,
    0x0C4941E2ADE834E3 : 1,
    0xDFB05B2382FFB81D : 2,
    0x9349325338EF36FE : 3,
}


fn_picotool = 'out_picotool.txt'
fn_diskfree = 'out_diskfree.txt'
fn_lsusb    = 'out_lsusb.txt'
fn_ptdetail = 'out_picotool_device_info.txt'

class UsbBusAddr:
  bus = 0
  addr = 0
  chipid = -1
  boardid = -1
  def __init__( self, _bus, _addr ):
    self.bus = int(_bus)
    self.addr = int(_addr)
  def __repr__(self):
    return f'bus {self.bus} addr {self.addr}   ' \
           f'chip-id {self.chipid:016x} board-id {self.boardid}'
  def __str__(self):
    return self.__repr__()

class MountPoint:
  device = ''
  mount = ''
  def __init__(self, _device, _mount):
    self.device = _device
    self.mount = _mount
  def __repr__(self):
    return f'device {self.device}, mount {self.mount}'
  def __str__(self):
    return self.__repr__()

class Details:
  bus = 0
  addr = 0
  vid = 0x0000
  pid = 0x0000
  name = ''
  serial = 0x0
  # --- these are added from picotool and diskfree output
  device = ''
  mount = ''
  
  def __init__( self, _bus, _addr, _vid, _pid, _name, _serial ):
    self.bus    = int(_bus)
    self.addr   = int(_addr) 
    self.vid    = int(_vid, 16)
    self.pid    = int(_pid, 16)
    self.name   = _name
    self.serial = int(_serial,16)
  def __repr__(self):
    return f'bus {self.bus}, addr {self.addr}, ' \
           f'vid:pid {self.vid:04x}:{self.pid:04x}, ' \
           f'name {self.name}, serial {self.serial:016x}'
  def __str__(self):
    return self.__repr__()









# RP2350 device at bus 1, address 40:
# RP2350 device at bus 1, address 34:
# RP2350 device at bus 1, address 35:
# RP2350 device at bus 1, address 13:
class PicoToolOut:
  fname = None
  def __init__( self, fname ):
    self.fname = fname
    self.usb_bus_addr = []
    with open(self.fname, 'r') as file:
      for line in file:
        # print(line.strip())
        words = line.strip().split()
        if words[0] != "RP2350": continue
        if words[3] != "bus": continue
        if words[5] != "address": continue
        bus = words[4].strip(',')
        addr = words[6].strip(':')
        self.usb_bus_addr.append( UsbBusAddr( bus, addr ))
  def __repr__(self):
    lines = [ str(u) for u in self.usb_bus_addr ]
    return '\n'.join( lines )
  def __str__(self):
    return self.__repr__()
  def check_bus_addr(self, b, a):
    for bus, addr in self.usb_bus_addr:
      if b == bus and a == addr: return true
    return false

# Multiple RP-series devices in BOOTSEL mode found:
# 
# RP2350 device at bus 1, address 40:
# -----------------------------------
# Device Information
#  type:                 RP2350
#  package:              QFN80
#  chipid:               0xdfb05b2382ffb81d
#  flash devinfo:        0x0c00
#  current cpu:          ARM
#  available cpus:       ARM, RISC-V
#  default cpu:          ARM
#  secure boot:          0
#  debug enable:         1
#  secure debug enable:  1
#  flash size:           16384K
# 
# RP2350 device at bus 1, address 34:
# -----------------------------------
# Device Information
#  type:                 RP2350
# ...etc...
def find_chipid( fname, b, a ):
  print(b,a)
  with open(fname, 'r') as file:
    found = False
    chipid = -1
    for line0 in file:
      line = line0.strip()
      if len(line)==0: continue
      #print(len(line), line.strip())
      words = line.split()
      print(found, len(words), words)
      if not found:
        if len(words) < 6: continue
        if words[0] != "RP2350": continue
        if words[1] != "device": continue
        if words[3] != "bus": continue
        if words[5] != "address": continue
        bus = int(words[4].strip(','))
        addr = int(words[6].strip(':'))
        if b != bus or a != addr: continue
        found = True # here, match is found
        continue
      else:
        print("*******")
        if words[0].startswith("chipid:"):
          print(words[1])
          chipid = int(words[1][2:],16)
          print(f'chipid  {chipid:016x}')
          break;
  return chipid



# /dev/disk6s1      134M    954k    133M     1%       0     0     -   /Volumes/RP2350 1
# /dev/disk7s1      134M    954k    133M     1%       0     0     -   /Volumes/RP2350 2
# /dev/disk8s1      134M    954k    133M     1%       0     0     -   /Volumes/RP2350 3
# /dev/disk5s1      134M    963k    133M     1%       0     0     -   /Volumes/RP2350
class DiskFreeOut:
  fname = None
  def __init__( self, fname ):
    self.fname = fname
    self.mounts = []
    with open(self.fname, 'r') as file:
      for line in file:
        #print(line.strip())
        # words = line.strip().split('  ')
        words = [ x.strip() for x in 
                 list(filter(None, line.strip().split('  '))) ]
        # print(words)
        device = words[0]
        mount = words[8]
        self.mounts.append( MountPoint( device, mount ))
  def __repr__(self):
    lines = [ str(m) for m in self.mounts ]
    return '\n'.join( lines )
  def __str__(self):
    return self.__repr__()

# Bus 001 Device 034: ID 2e8a:000f 2e8a RP2350 Boot  Serial: 9349325338EF36FE
# Bus 001 Device 040: ID 2e8a:000f 2e8a RP2350 Boot  Serial: DFB05B2382FFB81D
# Bus 001 Device 035: ID 2e8a:000f 2e8a RP2350 Boot  Serial: 0C4941E2ADE834E3
# Bus 001 Device 013: ID 2e8a:000f 2e8a RP2350 Boot  Serial: 7DF06CFA89A6F59A
class LsUsbOut:
  fname = None
  def __init__( self, fname ):
    self.fname = fname
    self.details = []
    with open(self.fname, 'r') as file:
      for line in file:
        #print(line.strip())
        words = line.strip(' ').split()
        # print(words)
        if not words[0].startswith("Bus"): continue
        if not words[2].startswith("Device"): continue
        if not words[4].startswith("ID"): continue
        if not words[8].startswith("Boot"): continue
        if not words[9].startswith("Serial"): continue
        bus    = words[1]
        addr   = words[3].strip(':')
        vidpid = words[5].split(':')
        vid    = vidpid[0]
        pid    = vidpid[1]
        name   = words[7]
        serial = words[10]
        self.details.append( Details( bus, addr, vid, pid, name, serial ))
  def __repr__(self):
    lines = [ str(u) for u in self.details ]
    return '\n'.join( lines )
  def __str__(self):
    return self.__repr__()


pt = PicoToolOut( fn_picotool )
df = DiskFreeOut( fn_diskfree )
ls = LsUsbOut(fn_lsusb );

# print(pt)
# print(df)
# print(ls)

for uba in pt.usb_bus_addr:
  chipid = find_chipid( fn_ptdetail, uba.bus, uba.addr )
  if chipid != -1: 
    print(f'{chipid:016x}')
    uba.chipid = chipid
    uba.boardid = serno_to_board_id[ chipid ]
