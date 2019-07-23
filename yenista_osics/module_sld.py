# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 16:47:10 2019

@author: qchat
"""

  

class SLD():   
    
    def __init__(self,dev,slot):
        
        self.dev = dev
        self.SLOT = slot
        
        self.dev.write(self.getPrefix()+'NM')
        self.dev.write(self.getPrefix()+'MW')
        
    #--------------------------------------------------------------------------
    # Optional functions
    #--------------------------------------------------------------------------
        
    def setSafeState(self):
        self.setOutputState(False)
        if self.getOutputState() is False :
            return True
            
        
    def getID(self):
        return self.dev.query(self.getPrefix()+'*IDN?')
        
        
    #--------------------------------------------------------------------------
    # Instrument variables
    #--------------------------------------------------------------------------
    
    def getPrefix(self):
        return f'CH{self.getSlotID()}:'
        
    def cleanResult(self,result):
        try:
            result=result.split(':')[1]
            result=result.split('=')[1]
            result=float(result)
        except:
            pass
        return result
    
    


    def getWavelength(self):
        return self.cleanResult(self.dev.query(self.getPrefix()+"L?"))
    
    
   
    
    
    def setPower(self,value):
        assert isinstance(float(value),float)
        value=float(value)
        if value < 5:
            self.setOutputState(False)
        elif 5<=value<10 :
            if self.getOutputState() is False :
                self.setOutputState(True)
            self.dev.write(self.getPrefix()+'P=LOW')
        else :
            if self.getOutputState() is False :
                self.setOutputState(True)
            self.dev.write(self.getPrefix()+'P=HIGH')        
        
    def getPower(self):
        ans=self.cleanResult(self.dev.query(self.getPrefix()+"P?"))
        if ans == 'Disabled':
            return 0
        elif ans == 'HIGH':
            return 10
        elif ans == 'LOW' :
            return 5
    
    
  
    
    
    
    def setOutputState(self,state):
        assert isinstance(state,bool)
        if state is True :
            self.dev.write(self.getPrefix()+"ENABLE")
        else :
            self.dev.write(self.getPrefix()+"DISABLE")
        
    def getOutputState(self):
        state=self.cleanResult(self.dev.query(self.getPrefix()+"ENABLE?"))
        if state == 'Enabled' :
            return True
        else :
            return False
    
        

    