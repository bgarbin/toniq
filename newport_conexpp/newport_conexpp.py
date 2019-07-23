# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""

from module_nsr1 import NSR1
import visa


ADDRESS = 'ASRL4::INSTR'
CALIBPATH_TIC = r'C:\Users\qchat\Documents\GitHub\local_config\NSR1_TIC_calib'
CALIBPATH_TAC = r'C:\Users\qchat\Documents\GitHub\local_config\NSR1_TAC_calib'


class Device():
    
    def __init__(self,address=ADDRESS,
                 calibpath_tic=CALIBPATH_TIC,
                 calibpath_tac=CALIBPATH_TAC):
        
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
        
        

    