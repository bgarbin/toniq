# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""

from telnetlib import Telnet
from module_ftb1750 import FTB1750

ADDRESS = '192.168.0.1'
PORT = 5024

class Device():
    
    def __init__(self,address=ADDRESS,port=PORT):
        
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
    
    
    




