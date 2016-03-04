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
from CaptureDigits import Part, capture, findNumbers
from digits import *
from DigitStat import FndN
import warnings 
print __doc__
def closeUp(cnt,db):
    ''' display a closeup view of a contour.'''
    img = np.zeros((120,960,3), np.uint8)          # empty black window   
    cv2.drawContours(img,[cnt],0,(255,255,255),1)
    imgx =    img.copy()
    cvs(db,imgx,'close up')
    
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

def evaluate( cnt1,db,cxcopy):
    ''' match the incomming contour against the set of digits we have stored in
        blobs.  '''
    cv2.drawContours(cxcopy,[cnt1],0,(255,255,0),2)
    cvs(1,cxcopy,'cxcopy')
    digits, labels =     cwload_digits("blobs\\aML*.png" )
    x,y,w,h = cv2.boundingRect(cnt1)   
    rn = [] 
    for xn,n in zip(digits,labels):                            
        #img = xn               # read a digit
        cvuint8 = cv2.convertScaleAbs(xn)
        img = cvuint8.copy()
        
        #cv2.imshow('return result',img)
        h,w = img.shape[:2]       
        ret, contours, hierarchy = cv2.findContours(cvuint8,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        cnt2 = contours[0]
        dist = cv2.matchShapes(cnt1,cnt2,1,0.0)
        area = cv2.contourArea(cnt1)
        if db: print 'dist from number {} is {}'.format( n, round(dist,5))
        rn.append( (dist,n) )     #  list of result from matchShapes 
        
    #  pick the one with the lowest score
    (dist,n) = min(rn, key = lambda (dist,n): dist )         #   minimum distence  
    if db: print 'rtn is {} dist {}  area {}'.format(n, round(dist,5),area)
    #  if the best one was close enough filter further based on number and area
    #  
    if (   dist >  36       
    or (   area <   150  )       
                         ):
        return(False,0,0)
    else:
        cv2.imshow('return result', img)
        print 'returning ', n, x,  w, h
        return(True,n,x)
    


def cwEvaluate(cnt,cmask ):
    ''' create set of test images for the SVN algorithm'''
    print ( len(cnt) , 'blobs to evaluate')
    digits, labels =     cwload_digits("blobs\\aML*.png" )
    digits2 = list(map(deskew, digits))
    samples = preprocess_hog(digits2)
    
    print('training SVM...')
    model = SVM(C=2.67, gamma=5.383)
    #print 'training labels',labels
    model.train(samples, labels) 
    dl = []
    for cn in cnt:                            #   each incomming digit
        x,y,w,h = cv2.boundingRect(cn)
        img = cmask[y:y+h,x:x+w].copy()
        img = np.float32(cv2.resize(img,(24,28) ))
        dl.append(img)
    digits = np.array(dl)
    #print digits
    digits2 = list(map(deskew, digits))        # no op unless it works 
    samples = preprocess_hog(digits2)
    print ('digit shape {} type {} samples shape {}'
             .format(digits.shape,digits.dtype ,samples.shape))
    resp = model.predict(samples)
    respI = map(int,resp)               #   return integer result
    return(respI)


def evalGame(ROI,db):
    ''' we obtain the ROI region of interest  from Part or as input from the
        last screen processed by Maintest.   We look for blob in the ROI and
        evaluate them by matching to our recorded set of captured digits.
    '''
 #   global db
    h,w = ROI.shape[:2]
    sROI =   cv2.resize(ROI,(3*w,3*h))        #    this may not be a good idea
    
    cxcopy = sROI.copy()    #   copy to mark up for display                                         # but we did it in CaptureDigits so .. .
    
    cmask,Scnt,hier = findNumbers(sROI)
    cvs(1,cxcopy,'cxcopy')
    #sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))     
    lxx = [] #cwEvaluate(Scnt,sROI)  #  pass contours to model -- returns result as list
    #return(lxx)
    print 'machine learn SVN',lxx
    lx = []
    for i, f in enumerate (Scnt):                  
        area = cv2.contourArea(f)
        x,y,w,h = cv2.boundingRect(f)        
        if area > 250 and hier[0][i][3] == -1 :         #  no parent
            possible = cmask[y:y+h, x:x+w].copy()       
            lb,n,t4S,t6LR,t7TB = FndN(possible,0,1)                  
            cv2.drawContours(cxcopy,[f],0,(255,255,0),1)    # draw after capture
            lx.append((x,n))
            if db: print '>>>match evaluate {}   <<<'.format(lx)
            cvs(1,cxcopy,'cxcopy')
    lx  =  sorted(lx,key = lambda (x,n):x )
    lx = [b for (a,b) in lx]
    return lxx  , lx                 # list of numbers in the panel

if  __name__ == '__main__':
    global db     
    db = 1
    fil = "pics\sc_sample_terran_177_438_101_129.png"
    fx1 = "pics\sc_sample_terran_1452_835_95_148.png"
    fx2 = 'pics\sc_sample_terran_302_1312_168_188.png'
    fx3 = "pics\sc_sample_terran_177_438_101_129.png"
    fx4 = "pics\sc_sample_terran_1087_267_67_94.png"
    for f in [fil] :  #,fx2,fx3,fx4]:
        h,w,ROI = Part(f,db)
    ##    cv2.imwrite('input.png',ROI)
        #  ROI   region of interest
        
    #    ROI = cv2.imread('input.png')    #   uses the last image from mainloop
     #   cvs(db, ROI, 'input')
        listx,listy = evalGame(ROI,db)
        print 'eval game SVN       ',listx    
        print 'eval game MatchShape',listy
        print f
    cvd()

    



