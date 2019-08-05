# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 08:51:25 2019

@author: qchat
"""

import visa
import time

ADDRESS = "ASRL5::INSTR"

class Device():
    
    def __init__(self,address=ADDRESS):
        
        rm = visa.ResourceManager()
        self.controller = rm.open_resource(address)
        self.controller.baud_rate = 57600
        self.controller.flow_control = visa.constants.VI_ASRL_FLOW_XON_XOFF





    def query(self,command,unwrap=True) :
        result = self.controller.query(self.SLOT+command)
        if unwrap is True :
            try:
                prefix=self.SLOT+command[0:2]
                result = result.replace(prefix,'')
                result = result.strip()
                result = float(result)
            except:
                pass
        return result
        
    def write(self,command) :
        self.controller.write(self.SLOT+command)
    
    
    
    

    def getState(self):
        ans = self.query('TS?',unwrap=False)[-2:]
        if ans[0] == '0' :
            return 'REF'
        elif ans == '14' :
            return 'CONF'
        elif ans in ['1E','1F'] :
            return 'HOMING'
        elif ans == '28' :
            return 'MOVING'
        elif ans[0] == '3' and ( ans[1].isalpha() is False)  :
            return 'ENABLED'
        elif ans[0] == '3' and ( ans[1].isalpha() is True)  :
            return 'DISABLED'
        else :
            return 'UNKNOWN'
        
        
            
    def checkNOTREFstate(self):
        
        # On vérifie que l'on est pas dans le mode REF
        state=self.getState()
        if state == 'REF' :
            self.write('OR') # Perfom Home search
            while self.getState() == 'HOMING' :
                time.sleep(0.5)
        elif state == 'CONF' :    
            self.write('PW0') # Sortie du mode Configuration
            self.checkNOTREFstate()
            
            
            
    def waitMoveEnding(self):
        while self.getFilterState() == 'MOVING' :
            time.sleep(0.1)
            
            
            
    def getID(self):
        return self.query('ID?')





    def getPosition(self):
        return self.query('PA?')
    
    def setPosition(self,value):
        self.setEnabled(True)
        self.write('PA'+str(value))
        self.waitMoveEnding()
        self.setEnabled(False)





    def goHome(self):
                            
        # Go to not ref mode
        self.write('RS')
        while self.getFilterState() != 'REF':
            time.sleep(0.1)
        
        # Homing to get back to ready state
        self.write('OR')
        while self.getFilterState() != 'ENABLED':
            time.sleep(0.1)

        # On le désactive
        self.setEnabled(False)
        while self.getFilterState() != 'DISABLED':
            time.sleep(0.1)
            
            
            
            

    def setEnabled(self,value):
        assert isinstance(bool(value),bool)
        self.write('MM'+str(int(value)))
    
    def isEnabled(self):
        state=self.getFilterState()
        if state in ['ENABLED','MOVING'] :
            return True
        else :
            return False
