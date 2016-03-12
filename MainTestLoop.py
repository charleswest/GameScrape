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
    db = 0
    dfile = 'digits.txt'
    fd = open(dfile,'w')
    fdbug = open('debug.txt', 'w')
    tfile = 'testFile.txt'           
    c = [0,0,0] ; f = [0,0,0]
    correct = 0; failed = 0;
    with open(tfile,'r' ) as fr:
        c = 0    #  total correct
        for i,line in enumerate(fr):  
            data,b,filen = line.split()     #  ignore b data for now    
            print 'file>>>>>>>> {}  '.format(filen)
            numbs = [int(x) for x in (data) if x  not in ['(', ',',')' ]]
##    now we know what to expect we shall see if we can find it
            h,w,ROI = Part(filen,db)           
            res =evalGame(ROI,fd,numbs,db)
            print 'evalGame returns ',res
            print ' input     was   ',numbs
            if res == numbs:
                c += 1
                print '****',
            else:
                #cv2.imwrite('input.png',ROI)   # save the problem page
                fdbug.write(line)
                for rn,n in zip(res,numbs):
                    if rn != n : print rn, n   #  highlight the problems
            p = 100.0 *c / (i+1)
            print '{} correct out of {}   {} pct'.format(c,1+i,round(p,2))
    fd.close()
##    prb = printsort()
##    print 'problems are', prb
    cvd()
            
             














 



