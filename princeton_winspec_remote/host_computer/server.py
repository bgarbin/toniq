#!/usr/bin/env python
import socket
import threading
import datetime as dt

from winspec import Winspec

class Server :
    
    def __init__(self):

        log('')
        log(' *** WINSPEC SERVER by Q.C., March 2019 *** ')
        log('')
        log('1) Start Winspec')
        log('2) Close other windows')
        log('3) Start Winspec server')
        log('')
        log('Server starting...')
    
        self.ip = '192.168.0.3'
        self.port = 5005    
        
        self.winspec = Winspec()
    
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip, self.port))
        self.s.listen(1)

        self.thread = None
        
        log('Ok ! Server running. Waiting for an incoming connection...')
        
        while True :
            conn, addr = self.s.accept()
            if self.thread is not None : 
                self.thread.stopFlag.set()
            self.thread = ClientThread(conn,self)
            self.thread.start()
            log('Incoming connection from '+str(addr))




def log(message):
    print(str(dt.datetime.now())+': '+message)




class ClientThread(threading.Thread):

    def __init__(self, clientsocket, server):

        self.server = server 
        
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        self.stopFlag = threading.Event()
        
    def run(self): 
        while True :
            try : 
                data = self.clientsocket.recv(1024)
            except : 
                break 
            
            if not data or self.stopFlag.isSet() : break
            
            command = data.decode()
            log('Received: '+str(command))
            
            answer = self.server.winspec.command(command)
            
            log('Sent: '+str(answer))
            
            self.clientsocket.send(str(answer).encode())  # echo

        self.clientsocket.close()
        log('Current connection closed')




server = Server()
