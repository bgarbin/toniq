#!/usr/bin/env python3

import visa as v
from optparse import OptionParser
import sys
import time
from numpy import zeros,ones,linspace

IP = '172.24.23.119'

class Device():
    def __init__(self,query=None,command=None,host=IP,offset=None,amplitude=None,frequency=None,ramp=None):

        rm = v.ResourceManager('@py')
        self.inst = rm.get_instrument('TCPIP::'+host+'::INSTR')
        
        if query:
            print('\nAnswer to query:',query)
            rep = self.query(query)
            print(rep,'\n')
            self.exit()
        elif command:
            print('\nExecuting command',command)
            self.write(command)
            print('\n')
            self.exit()
        
        if amplitude:
            self.amplitude(amplitude)
        if offset:
            self.offset(offset)
        if frequency:
            self.frequency(frequency)
        if ramp:
            self.ramp(ramp)
        
        self.exit()
    
    
    def amplitude(self,amplitude):
        self.inst.write('VOLT '+amplitude)
    def offset(self,offset):
        self.inst.write('VOLT:OFFS '+offset)
    def frequency(self,frequency):
        self.inst.write('FREQ '+frequency)
    
    def ramp(self,ramp):
        l   = list(zeros(5000) - 1)
        lll = list(ones(5000))
        ll  = list(linspace(-1,1,100+ramp))
        l.extend(ll);l.extend(lll)
        s = str(l)[1:-1]
        self.inst.write('DATA VOLATILE,'+s)
    
    def query(self,query):
        self.write(query)
        return self.read()
    def write(self,query):
        self.inst.write(query)
    def read(self):
        rep = self.inst.read()
        return rep
    def exit(self):
        sys.exit()
    def idn(self):
        self.inst.write('*IDN?')
        self.read()
        
            
if __name__ == '__main__':

    usage = """usage: %prog [options] arg
               
               
               EXAMPLES:
                   


               """
    parser = OptionParser(usage)
    parser.add_option("-c", "--command", type="str", dest="com", default=None, help="Set the command to use." )
    parser.add_option("-q", "--query", type="str", dest="que", default=None, help="Set the query to use." )
    parser.add_option("-r", "--ramp", type="float", dest="ramp", default=None, help="Turn on ramp mode." )
    parser.add_option("-o", "--offset", type="str", dest="off", default=None, help="Set the offset value." )
    parser.add_option("-a", "--amplitude", type="str", dest="amp", default=None, help="Set the amplitude." )
    parser.add_option("-f", "--frequency", type="str", dest="freq", default=None, help="Set the frequency." )
    parser.add_option("-i", "--ip_address", type="str", dest="ip_address", default=IP, help="Set the Ip address to use for communicate." )
    (options, args) = parser.parse_args()
    
    ### Start the talker ###
    Device(query=options.que,command=options.com,host=options.ip_address,ramp=options.ramp,offset=options.off,amplitude=options.amp,frequency=options.freq)
