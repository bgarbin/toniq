# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 22:22:53 2019

@author: quentin.chateiller
"""
import socket 

class WinspecConnector :
    
    def __init__(self):
        
        self.ADDRESS = '192.168.0.3'
        self.PORT = 5005
        self.BUFFER_SIZE = 40000
        
        self.controller = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.controller.connect((self.ADDRESS,self.PORT))        
        
    def write(self,command):
        self.controller.send(command.encode())
        self.controller.recv(self.BUFFER_SIZE)
        
    def query(self,command):
        self.controller.send(command.encode())
        data = self.controller.recv(self.BUFFER_SIZE)
        return data.decode()
        
    def close(self):
        try :
            self.controller.close()
        except :
            pass
        self.controller = None
