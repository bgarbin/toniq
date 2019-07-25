# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""
import visa

from module_sld import SLD
from module_t100 import T100

ADDRESS = 'GPIB0::15::INSTR'

modules_dict = {'sld':SLD,'t100':T100}

class Device():

    def __init__(self,address=ADDRESS,**kwargs):
        
        self.TIMEOUT = 1000 #ms
        
        rm = visa.ResourceManager()
        self.controller = rm.open_resource(address)
        self.controller.timeout = self.TIMEOUT
        
        # Submodules
        prefix = 'slot'
        for key in kwargs.keys():
            if key.startswith(prefix):
                slot_num = key[len(prefix):]
                module = modules_dict[ kwargs[key].split(',')[0].strip() ]
                name = kwargs[key].split(',')[1].strip()
                setattr(self,name,module(self,slot_num))


        
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






        
    
    
  
  