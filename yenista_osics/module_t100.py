# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 16:45:47 2019

@author: qchat
"""
import time

class T100():   
    
    def __init__(self,dev,slot):
        
        self.dev = dev
        self.SLOT = slot

        self.dev.write(self.SLOT+self.getPrefix()+'NM')
        self.dev.write(self.SLOT+self.getPrefix()+'MW')
    
    
    def setSafeState(self):
        self.setOutputState(False)
        if self.getOutputState() is False :
            return True
            

    def getID(self):
        return self.cleanResult(self.dev.query(self.SLOT+self.getPrefix()+'*IDN?'))
        
        
    #--------------------------------------------------------------------------
    # Instrument variables
    #--------------------------------------------------------------------------
    
    def getPrefix(self):
        return f'CH{self.SLOT}:'
        
    def cleanResult(self,result):
        try:
            result=result.split(':')[1]
            result=result.split('=')[1]
            result=float(result)
        except:
            pass
        return result
    
    


    def setWavelength(self,value):
        assert isinstance(float(value),float)
        self.dev.write(self.SLOT+"L=%f"%float(value))
        while True :
            try :
                self.getFrequency()
                break
            except :
                pass
        
    def getWavelength(self):
        return self.cleanResult(self.query(self.SLOT+"L?"))
    
    
    
    
    def setFrequency(self,value):
        assert isinstance(float(value),float)
        self.dev.write(self.SLOT+"F=%f"%float(value))
        while True :
            try :
                self.getFrequency()
                break
            except :
                pass
        
    def getFrequency(self):
        return self.cleanResult(self.dev.query(self.SLOT+"F?"))
    
    
    
    
    def setPower(self,value):
        assert isinstance(float(value),float)
        value=float(value)
        if value == 0.:
            self.setOutputState(False)
        else :
            if self.getOutputState() is False :
                self.setOutputState(True)
            self.dev.write(self.SLOT+"P=%f"%float(value))
        time.sleep(0.4)
        
        
        
    def getPower(self):
        ans=self.cleanResult(self.dev.query(self.SLOT+"P?"))
        if ans == 'Disabled':
            return 0
        else :
            return ans
    

    
    def setIntensity(self,value):
        assert isinstance(float(value),float)
        if value == 0.:
            self.setOutputState(False)
        else :
            if self.getOutputState() is False :
                self.setOutputState(True)
            self.dev.write(self.SLOT+"I=%f"%float(value))
        
        
    def getIntensity(self):
        ans=self.cleanResult(self.dev.query(self.SLOT+"I?"))
        if ans == 'Disabled':
            return 0
        else :
            return ans
        
        
    
    
    
    def setCoherenceControlState(self,state):
        assert isinstance(state,bool)
        if state is True :
            self.dev.write(self.SLOT+'CTRL ON')
        else :
            self.dev.write(self.SLOT+'CTRL OFF')
        time.sleep(0.2)
    
    def getCoherenceControlState(self):
        state=self.cleanResult(self.dev.query(self.SLOT+'CTRL?'))
        return bool(int(state))
    
    
    
    
    def setAutoPeakFindControlState(self,state):
        assert isinstance(state,bool)
        if state is True :
            self.dev.write(self.SLOT+'APF ON')
        else :
            self.dev.write(self.SLOT+'APF OFF')
        time.sleep(0.2)
        
    def getAutoPeakFindControlState(self):
        state=self.cleanResult(self.dev.query(self.SLOT+'APF?'))
        return bool(int(state))
    
    
    
    
    
    def setOutputState(self,state):
        assert isinstance(state,bool)
        if state is True :
            self.dev.write(self.SLOT+"ENABLE")
        else :
            self.dev.write(self.SLOT+"DISABLE")
        
    def getOutputState(self):
        state=self.cleanResult(self.dev.query(self.SLOT+"ENABLE?"))
        if state == 'ENABLED' :
            return True
        else :
            return False
    