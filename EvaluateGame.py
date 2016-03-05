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


def evalGame(ROI,db):
    ''' we obtain the ROI region of interest  from Part or as input from the
        last screen processed by Maintest.   We look for blob in the ROI and
        evaluate them by matching to our recorded set of captured digits.
    '''
 #   global db
    h,w = ROI.shape[:2]
    sROI =   cv2.resize(ROI,(3*w,3*h))        #    this may not be a good idea    
    sROI = erode(sROI,1)
    cxcopy = sROI.copy()    #   copy to mark up for display                                         # but we did it in CaptureDigits so .. .
    cmask,Scnt,hier = findNumbers(sROI)
    cvs(1,cxcopy,'cxcopy')
    lx = [] ; ly = []
    for i, f in enumerate (Scnt):                  
        area = cv2.contourArea(f)
        x,y,w,h = cv2.boundingRect(f)
        cv2.drawContours(cxcopy,[f],0,(0,0,255),2)
        #print 'area {} hier {}'.format(area, hier [0][i]) 
        if (area > 250
            and hier[0][i][3] == -1
            and  x <> 363):        #  no parent
            possible = cmask[y:y+h, x:x+w].copy()       
            lb,n,t4S,t6LR,t7TB = FndN(possible,x,1)                  
            cv2.drawContours(cxcopy,[f],0,(0,255,0),1)    # draw after capture
            lx.append((x,n))
            ly.insert(0,n)                         # approximate order
            if db: print '>>>match evaluate {}   <<<'.format(ly)
        cvs(1,cxcopy,'cxcopy')
    lx  =  sorted(lx,key = lambda (x,n):x )
    lx = [b for (a,b) in lx]
    return  lx                 # list of numbers in the panel

if  __name__ == '__main__':
    global db     
    db = 0
    fx0 = "pics\sc_sample_terran_177_438_101_129.png"
    fx1 = "pics\sc_sample_terran_1452_835_95_148.png"
    fx2 = 'pics\sc_sample_terran_302_1312_168_188.png'
    fx3 = "pics\sc_sample_terran_177_438_101_129.png"
    fx4 = "pics\sc_sample_terran_1087_267_67_94.png"
    for f in [fx0,fx1,fx2,fx3,fx4] :  #,fx2,fx3,fx4]:
        h,w,ROI = Part(f,db)
        print '\tn \tt4S \tt6LR \tt7TB'
        listx = evalGame(ROI,db)
        print 'eval game Harr      ',listx    
        #print 'eval game MatchShape',listy
        print f
    cvd()

    



