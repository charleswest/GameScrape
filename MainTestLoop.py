"""
This program loads each image in the   directory
and reads the manifest to provide a score for the
evaluation
 
enter q to leave early
"""
import os
import glob
import time
import numpy as np
import cv2
from cwUtils import cvd, cvs
from findBlobs import findBlobs, boundsBlob, stdSize
from EvaluateGame import evalGame, Part
import warnings 
print __doc__
if  __name__ == '__main__':
    global db     
    db = 0
    tfile = 'testFile.txt'          #   may need some manual edits
    c = [0,0,0] ; f = [0,0,0]
    correct = 0; failed = 0;
    with open(tfile,'r' ) as fr:
        c = 0    #  total correct
        for i,line in enumerate(fr):  

            data,b,filen = line.split()     #  ignore b data for now    
            print 'file < {} >>>>>>>> {}  '.format(i+1 ,filen)            
            dn  = eval(data)
            print 'input was        ' , dn
##    now we know what to expect we shall see if we can find it           
            lx =evalGame(filen,db)
            print 'evalGame returns ',lx
            if lx == dn:
                c += 1
                print '****',       
                #cv2.imwrite('input.png',ROI)   # save the problem page
                 
            p = 100.0 *c / (i+1)
            print '{} correct out of {}   {} pct'.format(c,1+i,round(p,2))
            
    cvd()
            
             














 



