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
from cwUtils import cvd, cvs
from findBlobs import findBlobs, boundsBlob, stdSize
import warnings 
print __doc__
def Part(  fx,db):
    ''' partition the image and return the ROI '''
    img = cv2.imread(fx)
    h,w = img.shape[:2]
    #print 'image h {} w {}'.format(h,w)
    y1  = 0  ; y2 = int(.05 * h)
    x1  = int (.75 * w)  ; x2 = int(w)  
    ROI =  img[ y1:y2,    x1:x2 ].copy()
    return(h,w,ROI)

def closeUp(cnt,db):
    ''' display a closeup view of a contour.'''
    img = np.zeros((120,960,3), np.uint8)          # empty black window   
    cv2.drawContours(img,[cnt],0,(255,255,255),1)
    imgx =    img.copy()
    cvs(db,imgx,'close up')
    

def evaluate( cnt1,db):
    ''' match the incomming contour against the set of digits we have stored in
        blobs.  '''
 #   global db
    closeUp(cnt1,db)
    path = ("blobs\\*.png" )                
    files = glob.glob(path)
    rn = [] 
    for n,f in enumerate(files):                
        #if db: print 'Blob  ', f[-5:-4],       
        img = cv2.imread(f,0)                  # read a digit 
        h,w = img.shape[:2]

        #print 'pixels {}, w {} h {} '.format( np.sum(img)/255,w,h) 
        ret, contours,hierarchy = cv2.findContours(img,2,1)
        cnt2 = contours[0]

        ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
        area = cv2.contourArea(cnt1)
        if db: print 'dist from number {} is {} area is {}'.format( n, round(ret,5),area)
        rn.append( (ret,n) )     #  list of result from matchShapes 
        
    #  sort all the results and pick the one with the lowest score
    rns = sorted (rn, key = lambda x:x[0])    
    if db: print 'rn is ',round(rns[0][0],5), rns[0][1], 'area' ,area
    #  if the best one was close enough filter further based on number and area
    #  
    if (  rns[0][0] >  .35          #.1:
    or    rns[0][1] == 4 and (area < 200 or area > 310)          
    or    rns[0][1] == 0 and area < 400 ):
        return(False,0)
    else:
        return(True,rns[0][1])
                    


def evalGame(ROI,db):
    ''' we obtain the ROI region of interest  from Part or as input from the
        last screen processed by Maintest.   We look for blob in the ROI and
        evaluate them by matching to our recorded set of captured digits.
    '''
 #   global db
    h,w = ROI.shape[:2]
    sROI =     cv2.resize(ROI,(2*w,2*h))        #    this may not be a good idea
                                             # but we did it in CaptureDigits so .. .
    ms = 100;   mx = 550; erd = 0; tx = 127
    # ms minimum size
    # erd erosion dilation -- leave this at zero
    # tx the threshold for the binary mask 
    (cnt,cmask) =  findBlobs(sROI,ms,mx,erd,0,tx) # will modify img to show cnt
    img2 = sROI.copy()    #   copy to mark up for display
    Scnt  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
    # sort left to right
    if db: print ' input is ms {} mx {} tval {}  count {} '\
          .format(ms,mx,tx, len(cnt))
    x,y,w,h = boundsBlob(cnt)    #    outer bounds of blob area
    if db: print (x,y,w,h)
    tl = (x-10,y-10) ; br = ( x  +  w+10, y+ h+10)       #  10 for more room
    cv2.rectangle(img2,(tl),(br),(255,255,255),1)         # white rectangle
    #cvs( db, img2, ' sROI')
    lx = []
    for i, f in enumerate (Scnt):       # scan left to right sorted contours             
       
        if db: print ' blob {}'.format(i),
        # compare blob to our file of tempate blobs 
        ret,n = evaluate(f,db)
        if ret:
            if db: print 'evaluate returns {}, number {}'.format(ret,n)
            cv2.drawContours(img2,[f],0,(0,255,0),1)    # draw after capture
            cmask = cmask -cmask
            cv2.drawContours(cmask,[f],0,(255,255,255),1)
            lx.append(n)
            #cvs(0,cmask,'cmask')
            cvs(db,img2,'evaluate')
            
    return lx                   # list of numbers in the panel

if  __name__ == '__main__':
    global db     
    db = 0
    fx = 'pics\sc_sample_terran_1087_267_67_94.png'
    h,w,ROI = Part(fx,db)
    
          #  ROI   region of interest
    ROI = cv2.imread('input.png')    #   uses the last image from mainloop
    cvs(db, ROI, 'input')
    listx = evalGame(ROI,db)
    print 'eval game returns',listx    
    cvd()

    



