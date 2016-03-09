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
from CaptureDigits import Part, capture
from AnalyseDigits import  findNumbers
from DigitStat import identifyN, parm
from printsort import printsort
import warnings 
print __doc__

def evalGame(ROI,fd,rn,db):
    ''' we obtain the ROI region of interest  from Part or as input from the
        last screen processed by Maintest.   We look for blob in the ROI and
        evaluate them by matching to specific areas in the img.
    '''
    
    h,w = ROI.shape[:2]
    sROI =   cv2.resize(ROI,(3*w,3*h))        #    this may not be a good idea    
    sROI = erode(sROI,1)
    cxcopy = sROI.copy()    #   copy to mark up for display                                         # but we did it in CaptureDigits so .. .
    cmask,cnt,hier = findNumbers(sROI,db)    # incorporate hier check

    if db: print hier.shape, len(cnt)
    Scon  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
    
    cvs(db,cxcopy,'cxcopy')
    lx = [] ; ly = [] ; j = -1
    
    for i, f in enumerate (Scon):                  
        area = cv2.contourArea(f)
        x,y,w,h = cv2.boundingRect(f)
        cv2.drawContours(cxcopy,[f],0,(0,0,255),2)
        if (area > 250
            and  x <> 363 and x <> 774):       #  some bad blobs here     
            j = j + 1
            possible = cmask[y:y+h, x:x+w].copy()
            if j == len(rn):
                j = 1
                lbx = -1
            else:
                lbx = rn[j]
            if db: print 'possible n {} w {} h {}'.format(lbx ,w,h)    
            parm.lst  = identifyN(possible,lbx,db)
            n = parm.lst[1]
            fd.write('{} \n'.format(parm.lst ))
            cv2.drawContours(cxcopy,[f],0,(0,255,0),1)    # draw after capture
            lx.append((x,n))
            ly.append(n)                         # approximate order
            if db: print '>>>match evaluate {}   <<<'.format(ly)
        cvs(db,cxcopy,'cxcopy')
    lx  =  sorted(lx,key = lambda (x,n):x )
    lx = [b for (a,b) in lx]
    return  lx                 # list of numbers in the panel

if  __name__ == '__main__':
    global db     
    db = 1
    fx0 = "pics\sc_sample_terran_177_438_101_129.png"
    fx1 = "pics\sc_sample_terran_1452_835_95_148.png"
    fx2 = 'pics\sc_sample_terran_302_1312_168_188.png'
    fx3 = "pics\sc_sample_terran_177_438_101_129.png"
    fx4 = "pics\sc_sample_terran_1087_267_67_94.png"

    rn0 = '177438101129'
    rn1 = '145283595148'
    rn4 = '10872676794'
    dfile = 'digits.txt'
    fd = open(dfile,'w')
    for f,rn in zip( [fx1 ],[rn1 ]):    #,fx2,fx3,fx4] :  #,fx2,fx3,fx4]:
        h,w,ROI = Part(f,db)
        listx = evalGame(ROI,fd,rn,db)    #  ::-1 is string reverse
        print 'eval game Harr   ',listx
        print ' rn value was    ',map(int,list(rn))
        #print 'eval game MatchShape',listy
        print f
        
    fd.close()
    printsort()
    cvd()

    



