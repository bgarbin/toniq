# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""
import visa
import time 
import os

import numpy as np
import pandas as pd

class Device():
    
    def __init__(self,address):
        
        self.ADDRESS = address
        self.BAUDRATE = 115200
        self.TIMEOUT = 1000 #ms
        
        # Initialisation
        rm = visa.ResourceManager()
        self.controller = rm.open_resource(self.ADDRESS)
        self.controller.timeout = self.TIMEOUT
        
        # Subdevices
        self.tic = NSR1(self,'tic')
        self.tac = NSR1(self,'tac')
        
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
        
        

    
    


slot = {'tic':1,'tac':2}
        

class NSR1():
    
    def __init__(self,dev,name):
        
        self.dev = dev
        self.NAME = name
        self.SLOT = slot[self.NAME]
        
        self.calib = None
        self.loadCalib()
        
        
    def query(self,command,unwrap=True) :
        result = self.dev.query(self.SLOT+command)
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
        self.dev.write(self.SLOT+command)
    
       
    
            
    def getID(self):
        return self.query('ID?',unwrap=False)
    
    
    
    def getFilterState(self):
        ans = self.query('TS?',unwrap=False)[-2:]
        if ans[0] == '0' :
            return 'REF'
        elif ans == '14' :
            return 'CONF'
        elif ans == '1E' :
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
        state=self.getFilterState()
        if state == 'REF' :
            self.write('OR') # Perfom Home search
            while self.getFilterState() == 'HOMING' :
                time.sleep(0.5)
        elif state == 'CONF' :    
            self.write('PW0') # Sortie du mode Configuration
            self.checkNOTREFstate()
            
    def waitMoveEnding(self):
        while self.getFilterState() == 'MOVING' :
            time.sleep(0.1)

    
    
    
    def setEnabled(self,value):
        assert isinstance(bool(value),bool)
        self.checkNOTREFstate()                
        self.write('MM'+str(int(value)))
    
    def isEnabled(self):
        state=self.getFilterState()
        if state in ['ENABLED','MOVING'] :
            return True
        else :
            return False
        
        

        
        
    #--------------------------------------------------------------------------
    # Instrument variables
    #--------------------------------------------------------------------------
    
    
 
    
    def setVelocity(self,value):
        
        assert isinstance(int(value),int)
        value=int(value)
        
        if value != self.getVelocity():
            
            # Go to not ref mode
            self.write('RS')
            while self.getFilterState() != 'REF':
                time.sleep(0.1)
            
            # Go to config mode
            self.write('PW1')
            while self.getFilterState() != 'CONF':
                time.sleep(0.1)
            
            # Change value
            self.write('VA%i'%value)

            # Sortie du mode config
            self.write('PW0')
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
    
    def getVelocity(self):
        return self.query('VA?')
    
    
    def setAcceleration(self,value):
        
        assert isinstance(int(value),int)
        value=int(value)
        
        if value != self.getVelocity():
            
            # Go to not ref mode
            self.write('RS')
            while self.getFilterState() != 'REF':
                time.sleep(0.1)
            
            # Go to config mode
            self.write('PW1')
            while self.getFilterState() != 'CONF':
                time.sleep(0.1)
            
            # Change value
            self.write('AC%i'%value)

            # Sortie du mode config
            self.write('PW0')
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
    
        
    def getAcceleration(self):
        return self.query('AC?')
    
            
            
    
    
    
    def setAngle(self,value,forced=False):
        assert isinstance(float(value),float)
        value=float(value)
        
        if forced is False :
            currAngle = self.getAngle()
            if value > currAngle - 1.9 :
                self.setAngle(value+20,forced=True)
            
        self.setEnabled(True)
        self.write('PA'+str(value))
        self.waitMoveEnding()
        self.setEnabled(False)
        
    def getAngle(self):
        value = self.query('TP?')
        return value
       
    
    
    
    
    
    def setMin(self):
        self.setTransmission(0)
        
    def setMax(self):
        self.setTransmission(1)





    def setTransmission(self,value):
        assert isinstance(float(value),float)
        value = float(value)
        angle = self.getAngleFromTransmission(value)
        self.setAngle(angle)
    
    def getTransmission(self):
        angle = self.getAngle()
        return self.getTransmissionFromAngle(angle) 

    def getTransmissionMax(self):
        return max(self.calib['transmission'].max())



    def getAngleFromTransmission(self,value):
        ind = abs(self.calib['transmission']-value).idxmin()
        return float(self.calib.loc[ind,'angle'])   
    
    def getTransmissionFromAngle(self,value):
        ind = abs(self.calib['angle']-value).idxmin()
        return float(self.calib.loc[ind,'transmission'])   


    def getDataPath(self):
        if __name__ == '__main__' :
            return './{self.name}/'
        else :
            return os.path.join(os.path.dirname(os.path.realpath(__file__)),self.name)
        
    def loadCalib(self):
        dataPath = self.getDataPath()
        try : self.calib = pd.read_csv(os.path.join(dataPath),'data.csv')
        except : pass
        
    def setCalibrationData(self,angleList,TList):
        dataPath = self.getDataPath()
        data = pd.DataFrame()
        data.loc[:,'angle'] = angleList
        data.loc[:,'transmission'] = TList
        data.to_csv(os.path.join(dataPath),'data.csv')
        self.loadCalib()


    
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
            
            
