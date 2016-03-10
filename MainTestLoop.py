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
from EvaluateGame import evalGame, Part
from printsort import printsort
import warnings 
print __doc__
if  __name__ == '__main__':
    global db ,fd    
    db = 1
    dfile = 'digits.txt'
    fd = open(dfile,'w')
    tfile = 'testFile.txt'          #   may need some manual edits
    c = [0,0,0] ; f = [0,0,0]
    correct = 0; failed = 0;
    with open(tfile,'r' ) as fr:
        c = 0    #  total correct
        for i,line in enumerate(fr):  

            data,b,filen = line.split()     #  ignore b data for now    
            print 'file>>>>>>>> {}  '.format(filen)
            n  = eval(data)
            st = ''
            for x in n:                    # reformat data same as lx           
                st = st + str(x)
                lsst = list(st)
               
            
##    now we know what to expect we shall see if we can find it
            h,w,ROI = Part(filen,db)
            
            lx =evalGame(ROI,fd,lsst,db)
            lsst = map(int,lsst)
            print 'evalGame returns ',lx
            print ' input     was   ',lsst
            if lx == lsst:
                c += 1
                print '****',
            else:
                cv2.imwrite('input.png',ROI)   # save the problem page
                for rn,n in zip(lx,lsst):
                    if rn != n : print rn, n   #  highlight the problems
            p = 100.0 *c / (i+1)
            print '{} correct out of {}   {} pct'.format(c,1+i,round(p,2))
    fd.close()
    prb = printsort()
    print 'problems are', prb
    cvd()
            
             














 



