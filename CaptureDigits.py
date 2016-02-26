'''
This routine takes the imput full size photo and segments it .  As interesting numbers are outlined in green they can be captured and labeled with any number key or skipped
with any other key.  q will terminate the program.
More than one photo is required to capture all numbers.  Captured digits should be inspected and moved to the blobs sub directory
'''
import numpy as np
import cv2
from cwUtils import cvd, cvs
from findBlobs import findBlobs, boundsBlob, stdSize
import warnings

global db

def Part(  fx,db):
    ''' partition the image and return the ROI '''
    img = cv2.imread(fx)
    h,w = img.shape[:2]
    #print 'image h {} w {}'.format(h,w)
    y1  = 24  ; y2 = 48
     
    x1  =1516  ; x2 = 1920  ; d1 = 135; d2 = 200 ;d=300
  
    ROI =  img[ y1:y2,        1510:1585   ].copy()   # 177
    ROI1 = img[ y1:y2,        1650:1725  ].copy()     # 438
    ROI2 = img[ y1:y2,        1775:1900  ].copy()    # 101
    ROI3 = img[ y1:y2,        1820:1900  ].copy()    # 129
    
    
    return(h,w,ROI,ROI1,ROI2,ROI3)

def capture(f,j,mask,db):
    
    ''' write out the ith blob to a file'''
    x,y,w,h = cv2.boundingRect(f)
    blb =  mask[y-1:y+h+1, x-1:x+w+1].copy()     #   capture the thresholded img
                                                 #    with a 1 pxl border
   # x = cvs(1,blb,'blbx')
    cv2.imwrite('ablob{}.png'.format(j),blb)
    cvs(db,blb,'capture') 
  
if  __name__ == '__main__':
    print __doc__
    global db     
    db = 1
    fil = "pics\\sc_sample_terran_1087_267_67_94.png"
    #fil = 'input.png'
 
    h,w,c1,a,b,c = Part(fil,db)
    cvs(db,c1)
    cvs(db,a,'a')
    cvs(db,b,'b')
    cvs(db,c,'c')
    h,w = c1.shape[:2]
    cut = cv2.resize(c1,(2*w,2*h))  
    ms = 100;   mx = 500; erd = 0; tx = 127
    (cnt,cmask) =  findBlobs(cut,ms,mx,erd,db,tx) # will modify img to show cnt
    img2 = cut.copy()    #   copy to mark up for display
    cnt  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
    # sort left to right
    print ' input is   width {} height {} ms {} mx {} tval {}  count {} '\
          .format( w, h,ms,mx,tx, len(cnt))
    x,y,w,h = boundsBlob(cnt)    #    outer bounds of blob area
    print (x,y,w,h)
    tl = (x-10,y-10) ; br = ( x  +  w+10, y+ h+10)       #  10 for more room
    cv2.rectangle(img2,(tl),(br),(255,255,255),1)         # white rectangle
    
    for i, f in enumerate (cnt):                
        area = cv2.contourArea(f)
        print ' blob {} , area {}'.format(i,area)
        # capture blobs
                   
        cv2.drawContours(img2,[f],0,(0,255,0),3)    # draw after capture
        
        x = cvs(1,img2,'blobs')        # x is keypress from cvs
        if x in [1,2,3,4,5,6,7,8,9,0,'/' ] : capture(f,x,cmask)    # for ms = 50     
    cv2.imwrite('\pics\blobs.png',cut)
    cvd()
    print('end gam1')
    
    
