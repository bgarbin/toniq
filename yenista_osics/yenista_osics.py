# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""
import visa

from module_sld import SLD
from module_t100 import T100

class Device():

    def __init__(self,address='GPIB0::15::INSTR'):
        
        self.TIMEOUT = 1000 #ms
        
        rm = visa.ResourceManager()
        self.controller = rm.open_resource(address)
        self.controller.timeout = self.TIMEOUT
        
        self.sld = SLD(self,1)
        self.t100 = T100(self,2)

        
    def close(self):
        try : self.controller.close()
        except : pass

    def query(self,command):
        result = self.controller.query(command)
        result = result.strip('\n')
        if '=' in result : result = result.split('=')[1]
        try : result = float(result)
        except: pass
        return result
    
    def write(self,command):
        self.controller.write(command)
        
        
        
    def getID(self):
        return self.query('*IDN?')


    def setSafeState(self):
        self.sld.setSafeState()
        self.tec.setSafeState()






        
    
    
  
  