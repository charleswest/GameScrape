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
    y1  = .02 * h  ; y2 = int(.04 * h)
    x1  = int (.75 * w)  ; x2 = int(w)  
    ROI =  img[ y1:y2,    x1:x2 ].copy()
    return(h,w,ROI)
##def Part(  img,db):
##    h,w = img.shape[:2]
##    print 'image h {} w {}'.format(h,w)
##    y1  = .02 * h  ; y2 = int(.04 * h)
##    x1  = int (.75 * w)  ; x2 = int(w)  
## 
##    a =  img[ y1:y2,    x1:x2 ].copy()   
    
##    return([h,w,a])
def capture(f,j):
    ''' write out the ith blob to a file'''
    x,y,w,h = cv2.boundingRect(f)
    blb = cmask[y-1:y+h+1, x-1:x+w+1].copy()     #   capture the thresholded img
                                                 #    with a 1 pxl border
   # x = cvs(1,blb,'blbx')
    cv2.imwrite('ablob{}.png'.format(j),blb)
    cvs(db,blb,'capture') 
  
if  __name__ == '__main__':
    print __doc__
    global db     
    db = 0
    fil = "pics\sc_sample_terran_177_438_101_129.png"
    #fil = 'input.png'
 
    h,w,c1 = Part(fil,db)
    cvs(db,c1)
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
        if x in [1,2,3,4,5,6,7,8,9,0 ] : capture(f,x)    # for ms = 50     
    cv2.imwrite('\pics\blobs.png',cut)
    cvd()
    print('end gam1')
    
    
