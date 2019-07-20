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
        
        rm = visa.ResourceManager()
        self.controller = rm.open_resource(self.ADDRESS)
        self.controller.timeout = self.TIMEOUT
        
        self.askTimeList={}
        
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
        return self.query('ID')+' VER '+self.query('VER')





    def waitForMeasure(self,asker):
        
        if asker not in list(self.askTimeList):
            self.askTimeList[asker]=0
        
        timeConstant=self.getTimeConstant()
		
        while (time.time()-self.askTimeList[asker])<timeConstant*5:
            time.sleep(timeConstant/10)
                    
    def logMeasure(self,asker):
        self.askTimeList[asker]=time.time()




    def getMagnitude(self):
        self.waitForMeasure('magnitude') # remove because the gpib com time is already long enough..
        measure=float(self.query("MAG."))
        self.logMeasure('magnitude')
        
        return measure

    def getPhase(self):
        self.waitForMeasure('phase')
        measure=float(self.query("PHA."))
        self.logMeasure('phase')
        return measure
    
    def getRefFrequency(self):
        return float(self.query('FRQ.'))

    def getTimeConstant(self):
        return float(self.query('TC.'))
    
    def getSensitivity(self):
        return float(self.query('SEN.'))
    
    
    