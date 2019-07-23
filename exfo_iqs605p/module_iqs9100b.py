# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 16:39:47 2019

@author: qchat
"""

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
        