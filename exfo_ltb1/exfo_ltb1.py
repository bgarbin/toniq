# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""

from telnetlib import Telnet

class Device():
    
    def __init__(self,address='192.168.0.1',port=5024):
        
        self.TIMEOUT = 2 #s
        
        # Instantiation
        self.controller = Telnet(address,port)
        self.read()
        self.read()
        
        # Subdevices
        self.slot1 = FTB1750(self,1)
        self.slot2 = FTB1750(self,2)
        
    # -------------------------------------------------------------------------
    # Read & Write
    # -------------------------------------------------------------------------
    
    def write(self,command):
        try : self.controller.write(f'{command}\r\n'.encode())
        except : pass
        return self.read()
        
        
    def read(self):
        try :
            ans = self.controller.read_until('READY>'.encode(),timeout=self.TIMEOUT)
            ans = ans.decode().replace('READY>','').strip() 
            assert ans != ''
            return ans
        except :
            pass
        
    def close(self):
        try : self.controller.close()
        except : pass
    
    
    
        
        
        
    def getID(self):
        return self.write('*IDN?')
    
    
    




class FTB1750():
    
    def __init__(self,dev,slot):
        
        self.dev = dev
        self.SLOT = slot
        
        # Initialisation
        self.dev.write(f"LINS1:UNIT{self.SLOT}:POW W")                # Unité = Watts
        self.dev.write(f"LINS1:SENS{self.SLOT}:POW:RANG:AUTO 1")      # Ajuster la gamme de mesure automatiquement
        self.dev.write(f"LINS1:SENS{self.SLOT}:POW:REF:STAT 0")       # Set Absolute power measurment mode (dBm or W)
    
    

    
    def setAveragingState(self,state):
        assert isinstance(state,bool)
        currentState=self.getAveragingState()
        if state != currentState :
            state = int(state)
            self.dev.write(f"LINS1:SENS{self.SLOT}:AVER:STAT {state}")
    
    def getAveragingState(self):
        ans = self.dev.write(f"LINS1:SENS{self.SLOT}:AVER:STAT?")
        return bool(int(ans))



    
    
    def getBufferSize(self):
        ans = self.dev.write(f"LINS1:SENS{self.SLOT}:AVER:COUN?")
        return int(ans)
    
    def setBufferSize(self, value):
        assert isinstance(int(value),int)
        value=int(value)
        currentSize=self.getBufferSize()
        if currentSize != value :
            self.dev.write(f"LINS1:SENS{self.SLOT}:AVER:COUN {value}")


 
       

    
    def getPower(self):
        ans = self.dev.write(f"LINS1:READ{self.SLOT}:SCAL:POW:DC?")
        return float(ans)
    

    
        
    def setWavelength(self,wavelength):
        assert isinstance(float(wavelength),float)
        wavelength=float(wavelength)
        currentWavelength=self.getWavelength()
        if wavelength != currentWavelength :
            self.dev.write(f"LINS1:SENS{self.SLOT}:POW:WAV {wavelength} nm")

    
    def getWavelength(self):
        ans = self.dev.write(f"LINS1:SENS{self.SLOT}:POW:WAV?")
        return float(ans)
    
    
