#   To check address: sudo i2cdetect -y 1

import smbus
import time

class PCF8591:

  def __init__(self,address):
    self.bus = smbus.SMBus(1)
    self.address = address

  def read(self,chn): #channel
      try:
          self.bus.write_byte(self.address, 0x40 | chn)  # 01000000
          self.bus.read_byte(self.address) # dummy read to start conversion
      except Exception as e:
          print ("Address: %s \n%s" % (self.address,e))
      return self.bus.read_byte(self.address)

  def write(self,val):
      try:
          self.bus.write_byte_data(self.address, 0x40, int(val))
      except Exception as e:
          print ("Error: Device address: 0x%2X \n%s" % (self.address,e))

class Joystick:
  def __init__(self, address):
    self.adc = PCF8591(address)
  def getX(self):
    return(self.adc.read(1))
  def getY(self):
    return(self.adc.read(0))

joymove = Joystick(0x48)

try:

  while True:
    x = joymove.getX()
    y = joymove.getY()
    print(x, " , ", y)
    time.sleep(.1)

except KeyboardInterrupt: 
  print('\nExiting')
except Exception as e: # catch all other errors
  print('\n', e)

