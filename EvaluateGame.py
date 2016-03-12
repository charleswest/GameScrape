"""
This program loads each image in the   directory
and looks for numbers on the screen.
 
enter q leave early
'"""
import os
import glob
import time
import numpy as np
import cv2
from cwUtils import cvd, cvs,erode, dilate
from CaptureDigits import Part, capture, findNumbers

from DigitStat import identifyN, descriptor
from printsort import printsort
import warnings 
print __doc__

def evalGame(ROI,fd,rn,db):
    ''' we obtain the ROI region of interest  from Part or as input from the
        last screen processed by Maintest.   We look for blob in the ROI and
        evaluate them by matching to specific areas in the img.
    '''
    
    h,w = ROI.shape[:2]
 #   sROI =   cv2.resize(ROI,(3*w,3*h))        #    this may not be a good idea    
  
    cxcopy = ROI.copy()    #   copy to mark up for display                                         # but we did it in CaptureDigits so .. .
    cmask,cnt,hier = findNumbers(ROI,db)    # incorporate hier check
    if db: print hier.shape, len(cnt)
    Scon  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
    
    cvs(db,cxcopy,'cxcopy',3)
    lx = [] ; ly = [] ; j = -1
    
    for i, f in enumerate (Scon):                  
        area = cv2.contourArea(f)
        x,y,w,h = cv2.boundingRect(f)
        cv2.drawContours(cxcopy,[f],0,( 0,0,255),2)
        if db: print ' x {} contour  area {}'.format(x,area)
        if (area > 18
            and h >10
                    ):        
            j = j + 1
            possible = cmask[y:y+h, x:x+w].copy()
            if j == len(rn):
                j = 1;  lbx = -1      
            else:
                lbx = rn[j]
            if db: print ' x {} possible n {} w {} h {}'.format(x,lbx ,w,h)    
            descriptor.lst  = identifyN(possible,lbx,db)
            n = descriptor.lst[1]
            cvs(db,cxcopy,'cxcopy',3)
            cv2.drawContours(cxcopy,[f],0,(0,255,0),1)    # draw after capture
            if n <> -1:
                lx.append((x,n))
                ly.append(n)                         # approximate order
                fd.write('{} \n'.format(descriptor.lst ))
            if db: print '>>>match evaluate {}   <<<'.format(ly)
        cvs(db,cxcopy,'cxcopy',3)
    lx  =  sorted(lx,key = lambda (x,n):x )
    lx = [b for (a,b) in lx]
    return  lx                 # list of numbers in the panel

if  __name__ == '__main__':
    global db     
    db = 1               
    tfile = 'testFile.txt'     # file of all test cases 
    tfile = 'debug2.txt'        # file of problems from last main loop run
    fd = open('digits.txt','w')            #  write debug info
    with open(tfile,'r' ) as fr:    #  read input data    
        for i,line in enumerate(fr):  
            data,bdata,filen = line.split()     #  ignore b data for now    
            print 'file>>>>>>>> {}  '.format(filen)
            numbs = [int(x) for x in (data) if x  not in ['(', ',',')' ]]           
            ROI,ROIb = Part(filen,db)           
            print ('evalGame   ',evalGame(ROI,fd,numbs,db)  )
            print '  input         {} '.format(numbs), '\n'
            numbs = [int(x) for x in (bdata) if x  not in ['(', ',',')' ]]
            if numbs <> [0, 0, 0] :
                print  ('evalGame 2  ',evalGame(ROIb,fd,numbs,db)  )
                print '  input    2     {} '.format(numbs), '\n'
                
           
    cvd()

    



