#!/c/Python27/python.exe

import pvcam_Manis
import visa
from optparse import OptionParser
import sys
import subprocess
import time
from numpy import fromstring,int8,int16,float64,sign,savetxt

CAMERA = 'Camera1'
IP = 'ASRL6::INSTR'

class Device():
    def __init__(self,filename=None,camera_name=CAMERA,nb_frames=1,exposure=0.01,FORCE=False):
        self.pvcam = pvcam_Manis.Init_PVCam()
        
		### Initiate communication with the requested camera ###
        self.CAM = self.get_camera(camera_name=camera_name)

#        if query:
#            print('\nAnswer to query:',query)
#            rep = self.query(query)
#            print(rep,'\n')
#        elif command:
#            print('\nExecuting command',command)
#            self.scope.write(command)
#            print('\n')

        self.data = self.get_data(nb_frames=nb_frames,exposure=exposure)
        self.save_data(filename='test',camera_name=camera_name,FORCE=FORCE)
        
        sys.exit()

    def get_data(self, nb_frames=1, exposure=None, region=None, binning=None):
        data = self.CAM.acq(frames=nb_frames, exposure=exposure, region=region, binning=binning)
        data2 = [list(data[i].squeeze()) for i in xrange(len(data))]
        return data2

    def save_data(self,filename,camera_name=CAMERA,FORCE=False):
        # Verify file doesn't exist
        temp_filename = filename + '_spectro32' + camera_name + '.txt'
        #temp = subprocess.getoutput('ls').splitlines()
        #for i in range(len(temp)):
         #   if temp[i] == temp_filename and not(FORCE):
         #       print('\nFile ', temp_filename, ' already exists, use -F option, change filename or remove old file\n')
         #       sys.exit()
        self.lambd=[list(range(len(self.data[0])))]
        assert self.lambd, 'You may want to get_data before saving ...'
        [self.lambd.append(self.data[i]) for i in xrange(len(self.data))]
        f = savetxt(temp_filename,self.lambd)  ## squeeze
        print(camera_name + ' saved')

    def get_camera(self,camera_name='Camera1'):
        CAM = self.pvcam.PVCam.getCamera(camera_name)
        print('Got: %s' %camera_name)
        return CAM

    def list_cameras(self):
        return self.pvcam.listCameras()


if __name__=='__main__':

    usage = """usage: %prog [options] arg

               EXAMPLES:
                  
               

               """
    parser = OptionParser(usage)
    parser.add_option("-c", "--command", type="str", dest="com", default=None, help="Set the command to use." )
    parser.add_option("-q", "--query", type="str", dest="que", default=None, help="Set the query to use." )
    parser.add_option("-i", "--camera_name", type="string", dest="camera_name", default=CAMERA, help="Set camera to get" )
    parser.add_option("-n", "--nb_frames", type="int", dest="nb_frames", default=1, help="Set the number of frames" )
    parser.add_option("-e", "--exposure", type="float", dest="exposure", default=0.01, help="Set the time of exposure" )
    parser.add_option("-o", "--filename", type="string", dest="filename", default=None, help="Set the name of the output file" )
    parser.add_option("-F", "--force",action = "store_true", dest="force", default=False, help="Allows overwriting file" )
    (options, args) = parser.parse_args()
    
    ### Start the talker ###
    Device(filename=options.filename,camera_name=options.camera_name,nb_frames=options.nb_frames,exposure=options.exposure,FORCE=options.force)
    
