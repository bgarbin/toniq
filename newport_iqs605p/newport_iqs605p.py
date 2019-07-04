# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""

from telnetlib import Telnet

class Device():
    
    def __init__(self):
        
        self.IP ='192.168.0.99'
        self.PORT = 5024
        self.TIMEOUT = 2 #s
        
        # Instantiation
        self.controller = Telnet(self.IP,self.PORT)
        self.read()
        self.read()
        
        # Subdevice
        self.IQS9100B = IQS9100B(self,4)
        
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
        return self.query('*IDN?')
    
    
    




class IQS9100B():
    
    
    def __init__(self,dev,slot):
        
        self.dev = dev
        self.SLOT = slot
        
        # Initialisation
        self.dev.write(f'LINS1{self.SLOT}:STAT?')
        
        
    def setSafeState(self):
        self.setShutter(True)
        if self.isShuttered() is True :
            return True
        
        
        
    def setRoute(self,routeID):
        currRoute = self.getRoute()
        if currRoute != routeID :
            self.dev.write(f"LINS1{self.SLOT}:ROUT1:SCAN {int(routeID)}")
            self.dev.write(f'LINS1{self.SLOT}:ROUT1:SCAN:ADJ')

    def getRoute(self):
        ans=self.dev.write(f'LINS1{self.SLOT}:ROUT1:SCAN?')
        return int(ans)



    def isShuttered(self):
        ans=self.dev.write(f'LINS1{self.SLOT}:ROUT1:OPEN:STAT?')
        return not bool(int(ans))
        
    def setShutter(self,value):
        assert isinstance(value,bool)
        if value is False :
            self.dev.write(f"LINS1{self.SLOT}:ROUT1:OPEN")
        else :
            self.dev.write(f"LINS1{self.SLOT}:ROUT1:CLOS")
        