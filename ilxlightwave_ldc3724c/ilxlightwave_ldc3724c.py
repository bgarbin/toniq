# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""
import visa
import time 

ADDRESS = 'ASRL5::INSTR'

class Device():
    
    def __init__(self,address=ADDRESS):
        
        self.TIMEOUT = 15000 #ms
        
        # Instantiation
        rm = visa.ResourceManager()
        self.controller = rm.open_resource(address)
        self.controller.timeout = self.TIMEOUT
        
        # Initialisation
        self.write('*CLS')      # Clear status registers
        self.write('DELAY 0')   # User commands not delayed
        
        # Subdevices
        self.tec = TEC(self)
        self.las = LAS(self)
        
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
    
    
    



class LAS():
    
    def __init__(self,dev):
        
        self.dev = dev
        self.PRECISION = 0.1


    
    
    def getCurrent(self):
        self.dev.write('LAS:DIS:LDI')
        self.dev.query('*OPC?')
        return float(self.dev.query('LAS:LDI?'))

    def getCurrentSetpoint(self):
        return float(self.dev.query('LAS:SET:LDI?'))
        
    def setCurrent(self,value):
        assert isinstance(float(value),float)
        value = float(value)
        self.dev.write(f'LAS:LDI {value}')
        self.dev.write('LAS:DIS:SET')
        self.dev.query('*OPC?')
        if value > 0 :
            if self.isEnabled() is False :
                self.setEnabled(True)
            self.setMode('ILBW')
            self.waitForConvergence(self.getCurrent,value)
        elif value == 0 :
            if self.isEnabled() is True :
                self.setEnabled(False)




    def setPower(self,value):
        assert isinstance(float(value),float)
        value = float(value)
        self.dev.write(f'LAS:MDP {value}')
        self.dev.write('LAS:DIS:SET')
        self.dev.query('*OPC?')
        if value > 0 :
            if self.isEnabled() is False :
                self.setEnabled(True)
            self.setMode('MDP')
            self.waitForConvergence(self.getPower,value)
        elif value == 0 :
            if self.isEnabled() is True :
                self.setEnabled(False)

    def getPower(self):
        self.dev.write('LAS:DIS:MDP')
        self.dev.query('*OPC?')
        return float(self.dev.query('LAS:MDP?'))

    def getPowerSetpoint(self):
        return float(self.dev.query('LAS:SET:MDP?'))
    
    
    
    
    def setEnabled(self,value):
        assert isinstance(value,bool)
        self.dev.write(f'LAS:OUT {int(value)}')
        self.dev.query('*OPC?')
        if value is True :
            mode = self.dev.query('LAS:MODE?')
            if mode.startswith('I'):
                self.waitForConvergence(self.getCurrent,
                                        self.getCurrentSetpoint())
            elif mode.startswith('MD'):
                self.waitForConvergence(self.getPower,
                                        self.getPowerSetpoint())
        
    def isEnabled(self):
        return bool(int(self.dev.query('LAS:OUT?')))

    
    
    
    def waitForConvergence(self,func,setPoint):
        tini = time.time()
        while True :
            try : 
                if abs(func()-setPoint) < self.PRECISION*setPoint :
                    break
                else :
                    time.sleep(0.5)
            except :
                pass
            if time.time() - tini > 5 :
                break
            
            
            
            
    def setMode(self,mode):
        assert isinstance(mode,str)
        currMode = self.getMode()
        enabledMode = self.isEnabled()
        if currMode != mode :
            self.dev.write(f'LAS:MODE:{mode}')
            self.dev.query('*OPC?')
            self.setEnabled(enabledMode)
            
    def getMode(self):
        return self.dev.query('LAS:MODE?')
        
        
    
    
    
    
    



class TEC():
    
    def __init__(self,dev):
        
        self.dev = dev
        self.PRECISION = 0.05



    def getResistance(self):
        self.write('TEC:DIS:R')
        self.dev.query('*OPC?')
        return float(self.query('TEC:R?'))



    def setGain(self,value):
        assert isinstance(int(value),int)
        value = int(value)
        self.write(f'TEC:GAIN {value}')
        self.dev.query('*OPC?')
        
    def getGain(self):
        return int(float(self.query('TEC:GAIN?')))
   
    

    
    def getCurrent(self):
        self.dev.write('TEC:DIS:ITE')
        self.dev.query('*OPC?')
        return float(self.dev.query('TEC:ITE?'))

    def getCurrentSetpoint(self):
        return float(self.dev.query('TEC:SET:ITE?'))
        
    def setCurrent(self,value):
        assert isinstance(float(value),float)
        value = float(value)
        self.dev.write(f'TEC:ITE {value}')
        self.dev.write('TEC:DIS:SET')
        self.dev.query('*OPC?')
        if value > 0 :
            if self.isEnabled() is False :
                self.setEnabled(True)
            self.setMode('ITE')
            self.waitForConvergence(self.getCurrent,value)
        elif value == 0 :
            if self.isEnabled() is True :
                self.setEnabled(False)




    def setTemperature(self,value):
        assert isinstance(float(value),float)
        value = float(value)
        self.dev.write(f'TEC:T {value}')
        self.dev.write('TEC:DIS:SET')
        self.dev.query('*OPC?')
        if value > 0 :
            if self.isEnabled() is False :
                self.setEnabled(True)
            self.setMode('T')
            self.waitForConvergence(self.getTemperature,value)
        elif value == 0 :
            if self.isEnabled() is True :
                self.setEnabled(False)

    def getTemperature(self):
        self.dev.write('TEC:DIS:T')
        self.dev.query('*OPC?')
        return float(self.dev.query('TEC:T?'))

    def getTemperatureSetpoint(self):
        return float(self.dev.query('TEC:SET:T?'))
    
    

    
    
    def setEnabled(self,value):
        assert isinstance(value,bool)
        self.dev.write(f'TEC:OUT {int(value)}')
        self.dev.query('*OPC?')
        if value is True :
            mode = self.dev.query('TEC:MODE?')
            if mode.startswith('I'):
                self.waitForConvergence(self.getCurrent,
                                        self.getCurrentSetpoint())
            elif mode.startswith('T'):
                self.waitForConvergence(self.getTemperature,
                                        self.getTemperatureSetpoint())
        
    def isEnabled(self):
        return bool(int(self.dev.query('TEC:OUT?')))
    
    
    
    
    
    def waitForConvergence(self,func,setPoint):
        tini = time.time()
        while True :
            try : 
                if abs(func()-setPoint) < self.PRECISION*setPoint :
                    break
                else :
                    time.sleep(0.5)
            except :
                pass
            if time.time() - tini > 5 :
                break
            
            
            
            
    def setMode(self,mode):
        assert isinstance(mode,str)
        currMode = self.getMode()
        enabledMode = self.isEnabled()
        if currMode != mode :
            self.dev.write(f'TEC:MODE:{mode}')
            self.dev.query('*OPC?')
            self.setEnabled(enabledMode)
            
    def getMode(self):
        return self.dev.query('TEC:MODE?')
        
        
        
        