# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""
import visa

ADDRESS = 'GPIB0::9::INSTR'

class Device():
    
    def __init__(self,address=ADDRESS):
        
        self.TIMEOUT = 1000 #ms
        
        rm = visa.ResourceManager()
        self.controller = rm.open_resource(address)
        self.controller.timeout = self.TIMEOUT
        
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
    
    
    




    def setFrequency(self,value):
        self.write(f"F={value}")
        self.getFrequency()
        
    def getFrequency(self):
        return self.query("F?")




    def setWavelength(self,value):
        self.write(f"L={value}")
        self.getWavelength()
        
    def getWavelength(self):
        return self.query("L?")
    
    
    
    
    
    def setPower(self,value):
        self.write(f"P={float(value)}")
        if value == 0 : self.setOutput(False)
        else : 
            if self.getOutput() is False : self.setOutput(True)
        self.getPower()
        
    def getPower(self):
        ans=self.query("P?")
        if isinstance(ans,str) is True and ans == 'DISABLED' : return 0
        else : return ans
    



    def setIntensity(self,value):
        self.write("I=%f"%value)
        if value == 0 : self.setOutput(False)
        else :
            if self.getOutput() is False : self.setOutput(True)
        self.getIntensity()
        
    def getIntensity(self):
        ans=self.query("I?")
        if isinstance(ans,str) is True and ans == 'DISABLED' : return 0
        else : return ans
        
    
    
    
    def setOutput(self,state):
        assert isinstance(state,bool)
        if state is True : self.write("ENABLE")
        else : self.write("DISABLE")
        
    def getOutput(self):
        ans = self.query("P?")
        if isinstance(ans,str) is True and ans == 'DISABLED' : return False
        else : return True
        