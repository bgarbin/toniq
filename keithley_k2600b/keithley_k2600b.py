# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""
import visa

class Device():
    
    
    def __init__(self):
        
        self.ADDRESS = 'GPIB0::10::INSTR'
        self.TIMEOUT = 1000 #ms
        
        # Instantiation
        rm = visa.ResourceManager()
        self.controller = rm.open_resource(self.ADDRESS)
        self.controller.timeout = self.TIMEOUT
        
        # Initialisation
        self.write('*CLS')
        
        # Subdevices
        self.source1 = Line(self,1)
        self.source2 = Line(self,2)
        
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
        
    
    
    def setSafeState(self):
        self.source1.setSafeState()
        self.source2.setSafeState()
    
    def getID(self):
        return self.query('*IDN?')
        
        

class Line():
    
    def __init__(self,dev,slot):
        
        self.dev = dev
        self.SLOT = slot
        
        # Initialisation
        self.dev.write(f"smu{self.SLOT}.source.autorangev = smu{self.SLOT}.AUTORANGE_ON")
        self.dev.write(f"smu{self.SLOT}.source.autorangei = smu{self.SLOT}.AUTORANGE_ON")
    
    def setSafeState(self):
        self.setVoltage(0)
        if self.setOutputState() is True :
            return False
        
        
        
    #--------------------------------------------------------------------------
    # Instrument variables
    #--------------------------------------------------------------------------
        


    def getResistance(self):
        self.dev.write(f'display.smu{self.SLOT}.measure.func = display.MEASURE_OHMS')
        return float(self.dev.query(f"print(smu{self.SLOT}.measure.r())"))
    
    
    
    
    def getPower(self):
        self.dev.write(f'display.smu{self.SLOT}.measure.func = display.MEASURE_WHATTS')
        return float(self.dev.query(f"print(smu{self.SLOT}.measure.p())"))




    def setPowerCompliance(self,value):
        assert isinstance(float(value),float)
        value = float(value)
        self.dev.write("smu{self.SLOT}.source.limitp = {value}")
        
    def getPowerCompliance(self):
        return float(self.dev.query(f"print(smu{self.SLOT}.source.limitp)"))




    
    def getCurrent(self):
        self.dev.write(f'display.smu{self.SLOT}.measure.func = display.MEASURE_DCAMPS')
        return float(self.dev.query(f"print(smu{self.SLOT}.measure.i())"))
    
    def setCurrent(self,value):
        assert isinstance(float(value),float)
        value = float(value)
        self.dev.write(f"smu{self.SLOT}.source.func = smu{self.SLOT}.OUTPUT_DCAMPS")
        self.dev.write(f"smu{self.SLOT}.source.leveli = {value}")
#        if value != 0. and self.getOutputState() is False :
#            self.setOutputState(True)
#        if value == 0. and self.getOutputState() is True :
#            self.setOutputState(False)
            
            
            
            
            
    def setCurrentCompliance(self,value):
        assert isinstance(float(value),float)
        value = float(value)
        self.dev.write("smu{self.SLOT}.source.limiti = {value}")
        
    def getCurrentCompliance(self):
        return float(self.dev.query("print(smu{self.SLOT}.source.limiti)"))





    
    def getVoltage(self):
        self.dev.write(f'display.smu{self.SLOT}.measure.func = display.MEASURE_DCVOLTS')
        return float(self.dev.query(f"print(smu{self.SLOT}.measure.v())"))
    
    def setVoltage(self,value):
        assert isinstance(float(value),float)
        value = float(value)
        self.dev.write(f"smu{self.SLOT}.source.func = smu{self.SLOT}.OUTPUT_DCVOLTS")
        self.dev.write(f"smu{self.SLOT}.source.levelv = {value}")
#        if value != 0. and self.getOutputState() is False :
#            self.setOutputState(True)
#        if value == 0. and self.getOutputState() is True :
#            self.setOutputState(False)
            
            
            
    def setVoltageCompliance(self,value):
        assert isinstance(float(value),float)
        value = float(value)
        self.dev.write("smu{self.SLOT}.source.limitv = {value}")
        
    def getVoltageCompliance(self):
        return float(self.dev.query("print(smu{self.SLOT}.source.limitv)"))





        
    def getOutputState(self):
        ans = self.dev.query(f"print(smu{self.SLOT}.source.output)")
        return bool(int(float(ans)))
                
    def setOutputState(self,state):
        assert isinstance(state,bool)
        if state is True :
            self.dev.write(f"smu{self.SLOT}.source.output = smu{self.SLOT}.OUTPUT_ON")
        else :
            self.dev.write(f"smu{self.SLOT}.source.output = smu{self.SLOT}.OUTPUT_OFF") 
        
    
            

    
    def set4wireModeState(self,state):
        assert isinstance(state,bool)
        if state is True :
            self.dev.write(f'smu{self.SLOT}.sense = smu{self.SLOT}.SENSE_REMOTE')
        else :
            self.dev.write(f'smu{self.SLOT}.sense = smu{self.SLOT}.SENSE_LOCAL')  

    def get4wireModeState(self):
        result=int(float(self.dev.query(f"print(smu{self.SLOT}.sense)")))
        if result == 0 :
            return False
        else :
            return True
        