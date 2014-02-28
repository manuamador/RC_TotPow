# -*- coding: utf-8 -*-
"""
Reverberation chamber stirrer control module based on ModBus protocol

"""
import minimalmodbus
import time
from numpy import *

class Stirrer(minimalmodbus.Instrument):
    """ Stirrer modbus instrument.
    Args:
        * portname (str): port number
        *slaveaddress (int): RTU slave address (1)
    """
    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self,portname,slaveaddress)
        self.serial.baudrate = 9600
        #self.serial.parity = serial.PARITY_NONE
        self.serial.bytesize = 8
        self.serial.stopbits = 1
        self.serial.timeout = 0.05
    
    def reset(self):
        """ Go to 0 position"""
        self.write_long(57766,0)
        posmesuree=self.read_long(58144,3)     
        while posmesuree != 0:
            posmesuree=self.read_long(58144,3)            
            time.sleep(.5)
        print 'Reset OK' 
    
    def getPosition(self):
        """ return stirrer current position"""
        return self.read_long(58144,3)
    
    def setPosition(self,position):
        """ go to the given angle in degree"""
        self.write_long(57766,position*10,signed=True)      
        posmesuree=nan
        while posmesuree != position*10:
            posmesuree=self.read_long(58144,3)            
            time.sleep(.1)

