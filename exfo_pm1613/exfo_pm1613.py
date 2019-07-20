# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""
import visa
import time

class Device():
    
    def __init__(self,address):
        
        self.ADDRESS = address
        self.TIMEOUT = 1000 #ms
        
        # Instantiation
        rm = visa.ResourceManager()
        self.controller = rm.open_resource(self.ADDRESS)
        self.controller.timeout = self.TIMEOUT
        
        # Initialisation
        self.write('SENS:POW:RANG:AUTO 1')      # Ajuster la gamme de mesure automatiquement
        self.write('SENS:POW:REF:STAT 0')       # Set Absolute power measurment mode (dBm or W)
        self.write('SENS:POW W')                # Unité = Watts
        self.write('SENS:POW:UNIT W')
        
        
        
        
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
    
    
    

    

    
    def setAveragingState(self,state):
        assert isinstance(state,bool)
        currentState=self.getAveragingState()
        if state != currentState :
            self.write('SENS:AVER:STAT %i'%int(state))
    
    def getAveragingState(self):
        return bool(self.query('SENS:AVER:STAT?'))
    
    
    
    
    
    def setZero(self):
        self.write('SENS:CORR:COLL:ZERO')
    
    
    
    
    
    def getBufferSize(self):
        return int(self.query('SENS:AVER:COUN?'))
    
    def setBufferSize(self, value):
        assert isinstance(int(value),int)
        value=int(value)
        currentSize=self.getBufferSize()
        if currentSize != value :
            self.write('SENS:AVER:COUN %i'%value)
        
        
        

    def getPower(self):
        while True :
            result=self.query('READ:ALL:POW:DC?')
            if '!' in result :
                time.sleep(0.1)
            else :
                break
        return float(result)



    
        
    def setWavelength(self,wavelength):
        assert isinstance(float(wavelength),float)
        wavelength=float(wavelength)
        currentWavelength=self.getWavelength()
        if wavelength != currentWavelength :
            self.write('SENS:POW:WAVE %f'%wavelength)
    
    def getWavelength(self):
        return float(self.query('SENS:POW:WAVE?'))
