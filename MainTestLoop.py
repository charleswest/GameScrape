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
    fdbug = open('debug2.txt', 'w')
    tfile = 'testFile.txt'           
    correct = 0; failed = 0;
    with open(tfile,'r' ) as fr:
        c = 0    #  total correct
        for i,line in enumerate(fr):  
            data,bdata,filen = line.split()       
            print 'file>>>>>>>> {}  '.format(filen)
            numbs = [int(x) for x in (data) if x  not in ['(', ',',')' ]]
##    now we know what to expect we shall see if we can find it
            ROI,ROIb = Part(filen,db)     #   return both upper and lower b areas      
            res = evalGame(ROI,fd,numbs,db)
            print 'evalGame returns ',res
            print ' input     was   ',numbs
            
            if 0:    # if true   check both panels -- if 0 check only upper
                bnumbs = [int(x) for x in (bdata) if x  not in ['(', ',',')' ]]
                if bnumbs <> [0, 0, 0] :       # move along nothing to see here
                    res2 = evalGame(ROIb,fd,bnumbs,db)
                    print 'evalGame  2 ', res2 
                    print '  input   2  {} '.format(bnumbs), '\n'
                OK = (res,res2) == (numbs,bnumbs)
            else:
                OK = (res ) == (numbs )
            if OK:
                c += 1
                print '****',
            else:               
                fdbug.write(line)             # save the problem for later
                for rn,n in zip(res,numbs):
                    if rn != n : print rn, n   #  highlight the problems
            p = 100.0 *c / (i+1)
            print '{} correct out of {}   {} pct\n'.format(c,1+i,round(p,2))
    fd.close()
    fdbug.close()
    
    cvd()
            
             














 



