'''
This routine takes the imput full size photo and segments it .  As interesting numbers are outlined in green they can be captured and labeled with any number key or skipped
with any other key.  q will terminate the program.
More than one photo is required to capture all numbers.  Captured digits should be inspected and moved to the blobs sub directory
'''
import numpy as np
import cv2
from cwUtils import cvd, cvs, erode, dilate
from findBlobs import findBlobs, boundsBlob, stdSize
import warnings

global db

def Part(  fx,db):
    ''' partition the image and return the ROI '''
    img = cv2.imread(fx)
    h,w = img.shape[:2]
    #print 'image h {} w {}'.format(h,w)
    y1  = .02 * h  ; y2 = int(.04 * h)
    x1  = int (.79  * w)  ; x2 = int(w)

    
    ROI =  img[ 26:39,    1510:1900 ].copy()
     
     
##    ROI =  img[ y1:y2,        1510:1585  ].copy()   # 177
##    ROI1 = img[ y1:y2,        1650:1725  ].copy()   # 438
##    ROI2 = img[ y1:y2,        1775:1900  ].copy()   # 101
##    ROI3 = img[ y1:y2,        1820:1900  ].copy()   # 129
    
    return(h,w,ROI)

def capture(f,j,mask):
    global db
    ''' write out the ith blob to a file'''
    x,y,w,h = cv2.boundingRect(f)
#    blb =  mask[y-1:y+h+1, x-1:x+w+1].copy()     #   capture the thresholded img
    blb =  mask[y:y+h, x:x+w].copy()
    #    with a 1 pxl border
   # x = cvs(1,blb,'blbx')
    blb = erode(blb,2)
    cv2.imwrite('aMLblob{}.png'.format(j),blb)
    print 'number is ' , j
    M = cv2.moments(blb)
    
##    for m in sorted(M):
##        print m, M[m]
    for m in cv2.HuMoments(cv2.moments(mask)).flatten():
        print m
    blbx = cv2.resize(blb,(4*w,4*h))
    cvs(1,blbx,'capture')

def findNumbers(cut):
    cxcopy = cut.copy()
    cvs(1,cxcopy,'cxcopy')
    ms = 100;   mx = 1500; erd = 0; tx = 127
    img2 = cut.copy()    #   copy to mark up for display
    gray = cv2.cvtColor(cut,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    #cvs(1,blur,'blur image')

    ret,thresh = cv2.threshold(blur,127,255,cv2.THRESH_BINARY) 
    thresh = erode(thresh,1)   
    #thresh = dilate(thresh,2)
    cvs(1, thresh,'threshold')
    mask = thresh.copy()
    im2,cnt, hier= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)  
    return(mask,cnt,hier)

if  __name__ == '__main__':
    print __doc__
    global db     
    db = 0
    fil = "pics\sc_sample_terran_177_438_101_129.png"
    fil = "pics\sc_sample_terran_1452_835_95_148.png"
  #  fil = "pics\sc_sample_terran_1087_267_67_94.png"
    #fil = 'input.png'
 
    h,w,c1 = Part(fil,db)
    cvs(db,c1)
    h,w = c1.shape[:2]
    cut = cv2.resize(c1,(3*w,3*h))
    cxcopy = cut.copy()    
    img,cnt,hier = findNumbers(cut)
    print hier.shape, len(cnt)
    print 'next, prev, 1st c. , parent\n',hier
    for i, f in enumerate (cnt):                
        area = cv2.contourArea(f)
        print ' blob {}  {}  area {} '.format(i,hier[0][i],area  )
        cv2.drawContours(cxcopy,[f],0,(0,255,255),2)    # draw after capture
        if area > 150 and area < 1900:            
            x = cvs(1,cxcopy,'cxcopy')        # x is keypress from cvs
            print ' '
            if x in [1,2,3,4,5,6,7,8,9,0 ] : capture(f,x,img)    # for ms = 50     
    cv2.imwrite('\pics\blobs.png',cut)
    cvd()
    print('end gam1')
    
    
