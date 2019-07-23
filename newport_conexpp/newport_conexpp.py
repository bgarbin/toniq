# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""

from module_nsr1 import NSR1
import visa





class Device():
    
    def __init__(self,address='ASRL4::INSTR',
                 calibpath_tic=r'C:\Users\qchat\Documents\GitHub\local_config\NSR1_TIC_calib',
                 calibpath_tac=r'C:\Users\qchat\Documents\GitHub\local_config\NSR1_TAC_calib'):
        
        self.BAUDRATE = 115200
        self.TIMEOUT = 1000 #ms
        
        # Initialisation
        rm = visa.ResourceManager()
        self.controller = rm.open_resource(address)
        self.controller.timeout = self.TIMEOUT
        
        # Subdevices
        self.tic = NSR1(self,1,'tic',calibpath_tic)
        self.tac = NSR1(self,2,'tac',calibpath_tac)
        
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
        
        

    