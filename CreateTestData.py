"""
This program loads each image in the   directory
and looks for user input to create the manifest.
 
enter q leave early
'"""
import os
import glob
import time
import numpy as np
import cv2
from cwUtils import cvd, cvs
from findBlobs import findBlobs, boundsBlob, stdSize
import warnings 
print __doc__
def Part(  img,db):
    h,w = img.shape[:2]
    print 'image h {} w {}'.format(h,w)
    y1  = 0  ; y2 = int(.1 * h)
    x1  = int (.75 * w)  ; x2 = int(w)  
    a =  img[ y1:y2,    x1:x2 ].copy()
    return(h,w,a)
    
if  __name__ == '__main__':
   global db     
   db = 1
   manifest = 'testFile.txt'
   mdata = open(manifest,'w') 
   path = 'pics\sc*'   #os.getcwd() #get the current directory   
   files = glob.glob( path)
   for fx in files:
      img = cv2.imread(fx)
      h,w,ROI = Part(img,db)
      cvs(1, ROI, 'input')  #cv2.imshow('input',ROI)  # cvs(db,ROI)
      usr = raw_input('what numbers?')
      print fx , 'has', usr
      if usr == 'q':
         break
      print >> mdata, usr , fx      #   create a list of user anotated filenames
      cvd()
      
   mdata.close()
   cvd() 



