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
from common import clock, mosaic
from cwUtils import cvd, cvs,erode, dilate
from findBlobs import findBlobs, boundsBlob, stdSize
from CaptureDigits import Part, capture
from AnalyseDigits import  findNumbers
from digits import *
from DigitStat import FndN
from printsort import printsort
import warnings 
print __doc__

def cwload_digits(fn):
 #   print('loading {} ...'.format(fn))
    path = fn               
    files = glob.glob(path)
    dl = []; lbl = []
    for f in files:
        fn = int((f[-5:-4]))
        lbl.append(fn)                    #get n label from filename       
        img = cv2.imread(f,0)
        #img = erode(img,2)
        #print( 'im  shape {} {}'.format( fn ,img.shape)  )
        img = np.float32(cv2.resize(img,(40,35) ))
        # cv2.imwrite('ars'+fn+'.png',img)
        dl.append(img)
    digits = np.array(dl)
    labels = np.array(lbl)
    cv2.imshow('training set', mosaic(10, digits[:]))
 #   print 'training set labels', labels
    return(digits,labels)    


def evalGame(ROI,db,fd,rn):
    ''' we obtain the ROI region of interest  from Part or as input from the
        last screen processed by Maintest.   We look for blob in the ROI and
        evaluate them by matching to our recorded set of captured digits.
    '''
 #   global db
    h,w = ROI.shape[:2]
    sROI =   cv2.resize(ROI,(3*w,3*h))        #    this may not be a good idea    
    sROI = erode(sROI,1)
    cxcopy = sROI.copy()    #   copy to mark up for display                                         # but we did it in CaptureDigits so .. .
    cmask,cnt,hier = findNumbers(sROI)    # incorporate hier check

    print hier.shape, len(cnt)
    Scon  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
    
    cvs(1,cxcopy,'cxcopy')
    lx = [] ; ly = [] ; j = -1
    
    for i, f in enumerate (Scon):                  
        area = cv2.contourArea(f)
        x,y,w,h = cv2.boundingRect(f)
        cv2.drawContours(cxcopy,[f],0,(0,0,255),2)
        #print 'area {} hier {}'.format(area, hier [0][i])
        #print  'j is {} len rn {}'.format(j, len(rn))
        if (area > 250
            #and hier[0][i][3] == -1
            and  x <> 363 and x <> 774):        #  no parent
            j = j + 1
            possible = cmask[y:y+h, x:x+w].copy()
            if j == len(rn):
                j = 1
                lbx = -1
            else:
                lbx = rn[j]
            lb,n,t0,L,R,T,B,S,LR,TB,M3  = FndN(possible,lbx,1)
            fd.write('{} {} {} {} {} {} {} {} {} {} {} \n'.format(lb,n,t0,L,R,T,B,S,LR,TB,M3  ))
            cv2.drawContours(cxcopy,[f],0,(0,255,0),1)    # draw after capture
            lx.append((x,n))
            ly.append(n)                         # approximate order
            #if db: print '>>>match evaluate {}   <<<'.format(ly)
        cvs(1,cxcopy,'cxcopy')
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
    for f,rn in zip( [fx4 ],[rn4 ]):    #,fx2,fx3,fx4] :  #,fx2,fx3,fx4]:
        h,w,ROI = Part(f,db)
        listx = evalGame(ROI,db,fd,rn)    #  ::-1 is string reverse
        print 'eval game Harr   ',listx
        print ' rn value was    ',map(int,list(rn))
        #print 'eval game MatchShape',listy
        print f
        
    fd.close()
    printsort()
    cvd()

    



