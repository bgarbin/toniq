# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:36:53 2019

@author: quentin.chateiller
"""
import numpy as np
import time

class Device():
    
    def __init__(self,param=2):
        
        self.po = 1
        print('HEEEELLLLOOO',param)
    
    def getAmplitude(self):
        return np.random.uniform()
    
    def setAmplitude(self,value):
        print('hufheiughreugh '+str(value))
    
    def close(self):
        print('CLOSSSSEEEEDDD')
        
    def getPhase(self):
        return np.random.uniform()
    
    def doSth(self):
        time.sleep(1)
        print('action')