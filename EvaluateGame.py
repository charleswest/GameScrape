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
        cv2.drawContours(cxcopy,[f],0,(255,255,255),1)
        if db: print ' x {} contour  area {}'.format(x,area)
        if (area > 18 and h >10
        or  area > 15 and w <9 
            ):        #   18  ok except red panel needs 16
            j = j + 1
            possible = cmask[y:y+h, x:x+w].copy()
            if j == len(rn):
                j = 1;  lbx = -1      
            else:
                lbx = rn[j]
            if db: print ' x {} possible n {} w {} h {}'.format(x,lbx ,w,h)    
            parm.lst  = identifyN(possible,lbx,db)
            n = parm.lst[1]
            
            cv2.drawContours(cxcopy,[f],0,(0,255,0),1)    # draw after capture
            if n <> -1:
                lx.append((x,n))
                ly.append(n)                         # approximate order
                fd.write('{} \n'.format(parm.lst ))
            if db: print '>>>match evaluate {}   <<<'.format(ly)
        cvs(db,cxcopy,'cxcopy',3)
    lx  =  sorted(lx,key = lambda (x,n):x )
    lx = [b for (a,b) in lx]
    return  lx                 # list of numbers in the panel

if  __name__ == '__main__':
    global db     
    db = 1
   
    fx1 = "pics\sc_sample_terran_1452_835_95_148.png"
    fx2 = 'pics\sc_sample_terran_302_1312_168_188.png'
    fx3 = "pics\sc_sample_terran_177_438_101_129.png"
    fx4 = "pics\sc_sample_terran_1087_267_67_94.png"
    fx5 = "pics\sc_sample_zerg_99_20_19_18_red.png"
    fx6 = 'pics\sc_sample_terran_324_260_42_54.png'
    fx7 = 'pics\sc_sample_terran_1475_3612_200_200.png'
    fx8 = 'pics\sc_sample_terran_69_148_27_38.png'
    fx6 = 'pics\sc_sample_terran_324_260_42_54.png'
    fx6 = 'pics\sc_sample_terran_324_260_42_54.png'
    txt = 'ROI.png'
    
    rn1 = '145283595148'
    rn2 = '3021312168188'
    rn3 = '177438101129'
    rn4 = '10872676794'
    rn5 = '99201918'
    rn6 = '3242604254'
    rn7 = '14753612200200'
    rn8 = '691482738'
    dfile = 'digits.txt'
    fd = open(dfile,'w')
     
    
    for f,rn in zip( [fx5 ],[rn5 ]):    #,fx2,fx3,fx4] :  #,fx2,fx3,fx4]:
        h,w,ROI = Part(f,db)
        cvs(db,ROI,'roi',3)
        listx = evalGame(ROI,fd,rn,db)    #  ::-1 is string reverse
        print 'eval game Harr   ',listx
        print ' rn value was    ',map(int,list(rn))
        #print 'eval game MatchShape',listy
        print f
        
    fd.close()
    printsort()
    cvd()

    



