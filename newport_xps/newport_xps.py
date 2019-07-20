# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:06:08 2019

@author: quentin.chateiller
"""

from .XPSpython import XPSdriver
import time
import os
import pandas as pd

class Device():
    
    def __init__(self,address):
        
        self.IP = address
        self.PORT = 5001
        self.TIMEOUT = 2
        
        # Instantiation
        self.controller = XPSdriver()
        self.socketID = self.controller.TCP_ConnectToServer(self.IP,self.PORT,self.TIMEOUT)

        # Subdevice
        self.toc = NSR1(self,'NSR1_TOC')
        
    # -------------------------------------------------------------------------
    # Read & Write
    # -------------------------------------------------------------------------
    
    def isConnected(self):
        try :
            assert self.controller.FirmwareVersionGet(self.socketID) is not None
            return True
        except :
            return False
        
        
    def query(self,command,**kwargs):
        
        assert isinstance(command,list)
        assert hasattr(self.controller,command[0])

        if len(command)>1 :
            ans = getattr(self.controller,command[0])(self.socketID,*command[1:])
        else :
            ans = getattr(self.controller,command[0])(self.socketID)
            
        if ans[1] != '' :
            if len(ans)>2:
                return ans[1:]
            else :
                return ans[1]
        
    def close(self):
        try : self.controller.TCP_CloseSocket(self.socketId)
        except : pass
    
    
        
     


class NSR1():
    
    
    def __init__(self,dev,slot):
        
        self.dev = dev
        self.SLOT = slot
       
        self.calib = None
        self.loadCalib()
        
    #--------------------------------------------------------------------------
    # Optional functions
    #--------------------------------------------------------------------------
        
    def setSafeState(self):
        self.setMin()
        if self.getTransmission() < 0.2 :
            return True
            

        

        
    #--------------------------------------------------------------------------
    # Technical functions
    #--------------------------------------------------------------------------
    
    def getFilterState(self):
        state=self.dev.query(['GroupStatusGet',self.SLOT])
        
        if 0 <= state <= 9 :
            return 'NOTINIT'
        elif state == 42 :
            return 'NOTREF'
        elif state == 43 :
            return 'HOMING'
        elif state == 44 :
            return 'MOVING'
        elif 10 <= state <= 19 :
            return 'ENABLED'
        elif 20 <= state <= 39 :
            return 'DISABLED'
        else :
            return None
    
    def checkReady(self):
    
        if self.getFilterState() in ['ENABLED','DISABLED'] :
            return True 
        else :
            if self.getFilterState() == 'NOTINIT' :
                self.dev.query(['GroupInitialize',self.SLOT])
                if self.getFilterState() != 'NOTREF' :
                    return False
            if self.getFilterState() == 'NOTREF':
                self.dev.query(['GroupHomeSearch',self.SLOT])
                while self.getFilterState() == 'HOMING' :
                    time.sleep(0.5)
                if self.getFilterState() in ['ENABLED','DISABLED'] :
                    self.setEnabled(False)
                    return True
                else :
                    return False
                
    
    def waitMoveEnding(self):
        while self.getFilterState() == 'MOVING' :
            time.sleep(0.1)
        time.sleep(0.4) # Trop rapide sinon
        
        
        
        
        
        
    def setEnabled(self,state):
        assert isinstance(state,bool)
        if state is True :
            self.dev.query(['GroupMotionEnable',self.SLOT])
        else :
            self.dev.query(['GroupMotionDisable',self.SLOT])       

    def isEnabled(self):
        state=self.getFilterState()
        if state in ['ENABLED','MOVING'] :
            return True
        else :
            return False
        
        
        
        

    def setPositionerName(self,value):
        assert isinstance(value,str)
        self.setData('positionerName',value)
        
    def getPositionerName(self):
        if 'positionerName' not in self.getDataList() :
            self.setPositionerName('Pos')
        return self.getData('positionerName')
    
    
    
        
    #--------------------------------------------------------------------------
    # Instrument variables
    #--------------------------------------------------------------------------
    
    
    
    def getParameters(self):
        if self.checkReady() is True :
            params={}
            temp=self.dev.query(['PositionerSGammaParametersGet',self.SLOT+'.'+self.getPositionerName()])       
            params['velocity']=temp[0]
            params['acceleration']=temp[1]
            params['minJerkTime']=temp[2]
            params['maxJerkTime']=temp[3]
            return params
        else :
            raise ValueError('Not ready')
            
    def setParameters(self,params):
        if self.checkReady() is True :
            self.dev.query(['PositionerSGammaParametersSet',self.SLOT+'.'+self.getPositionerName(),
                                                             params['velocity'],
                                                             params['acceleration'],
                                                             params['minJerkTime'],
                                                             params['maxJerkTime']]) 
        else :
            raise ValueError('Not ready')






    def setVelocity(self,value):
        assert isinstance(float(value),float)
        value=float(value)
        params=self.getParameters()
        params['velocity']=value
        self.setParameters(params)
    
    def getVelocity(self):
        return float(self.getParameters()['velocity'])


        
    


    def setAcceleration(self,value):
        assert isinstance(float(value),float)
        value=float(value)
        params=self.getParameters()
        params['acceleration']=value
        self.setParameters(params)
    
    def getAcceleration(self):
        return float(self.getParameters()['acceleration'])
    



    
    
    def setAngle(self,value,forced=False):
        assert isinstance(float(value),float)
        value=float(value)
        
        if forced is False :
            currAngle = self.getAngle()
            if value > currAngle - 1.9 :
                self.setAngle(value+20,forced=True)
            
        if self.checkReady() is True :
            self.setEnabled(True)
            self.dev.query(['GroupMoveAbsolute',self.SLOT,[value]])
            self.waitMoveEnding()
            self.setEnabled(False)
        else :
            raise ValueError('Not ready')
        
    def getAngle(self):
        if self.checkReady() is True :
            value = float(self.dev.query(['GroupPositionCurrentGet',self.SLOT,1]))
            return value
        else :
            raise ValueError('Not ready')
    
    
    
    
    

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


    
      
    
    def setMin(self):
        self.setTransmission(0)
        
    def setMax(self):
        self.setTransmission(1)



            
    
    def goHome(self):
        
        self.setAngle(self.getAngle()+5) # In case we are at home - blocking
        
        # Go to not init
        self.dev.query(['GroupKill',self.SLOT])
        while self.getFilterState() != 'NOTINIT':
            time.sleep(0.1)
                            
        # Go from not init to ref mode
        self.dev.query(['GroupInitialize',self.SLOT])
        while self.getFilterState() != 'NOTREF':
            time.sleep(0.1)
        
        # Homing to get back to ready state
        self.dev.query(['GroupHomeSearch',self.SLOT])
        while self.getFilterState() != 'ENABLED':
            time.sleep(0.1)

        # On le désactive
        self.setEnabled(False)
        while self.getFilterState() != 'DISABLED':
            time.sleep(0.1)
            
    
    
    