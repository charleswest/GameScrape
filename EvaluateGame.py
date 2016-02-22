"""
This program loads each image in the   directory
and looks for user input to create the manifest.
 
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
    img = cv2.imread(fx)
    h,w = img.shape[:2]
    #print 'image h {} w {}'.format(h,w)
    y1  = 0  ; y2 = int(.05 * h)
    x1  = int (.75 * w)  ; x2 = int(w)  
    ROI =  img[ y1:y2,    x1:x2 ].copy()
    return(h,w,ROI)

def closeUp(cnt):
    ''' display a closeup view of a contour.'''
    fx = 'pics\sc_sample_terran_1087_267_67_94.png'      
    h,w,ROI = Part(fx,0)      #  ROI   region of inte
    h,w = ROI.shape[:2]
    img =     cv2.resize(ROI,(2*w,2*h)) 
    h,w = img.shape[:2]
    # print ' Closeup ', h,w
    img = img - img
    cv2.drawContours(img,[cnt],0,(255,255,255),1)
    imgx =    img.copy()
  #  imgy =  cv2.resize(img, ( nw, int (nh) )  ) 
    cvs(1,imgx,'close up')
    

def evaluate( cnt1,db):
 #   global db
    closeUp(cnt1)
    path = ("blobs\\*.png" )                
    files = glob.glob(path)
    rn = [] 
    for n,f in enumerate(files):                
        #if db: print 'Blob  ', f[-5:-4],       
        img = cv2.imread(f,0)
        h,w = img.shape[:2]

        #print 'pixels {}, w {} h {} '.format( np.sum(img)/255,w,h) 
        ret, contours,hierarchy = cv2.findContours(img,2,1)
        cnt2 = contours[0]

        ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
        area = cv2.contourArea(cnt1)
        if db: print 'dist from number {} is {} area is {}'.format( n, round(ret,5),area)
        rn.append( (ret,n) )
        
    #  sort all the results and pick the one with the lowest score
    rns = sorted (rn, key = lambda x:x[0])    
    print 'rn is ',round(rns[0][0],5), rns[0][1], 'area' ,area
    #  if the best one was close enough filter further based on number and area  
    if rns[0][0] <  .35:   #.1:
        if rns[0][1] == 4 and (area < 200 or area > 310):
            return(False,0)
        elif rns[0][1] == 0 and area < 400:
            return(False,0)
        else:
            return(True,rns[0][1])
    else:
        return(False,0)                      #   the blob is not a digit


def evalGame(ROI,db):
 #   global db
    h,w = ROI.shape[:2]
    sROI =     cv2.resize(ROI,(2*w,2*h))        #    this may not be a good idea
                                             # but we did it in CaptureDigits so .. .
    ms = 100;   mx = 550; erd = 0; tx = 127
    (cnt,cmask) =  findBlobs(sROI,ms,mx,erd,0,tx) # will modify img to show cnt
    img2 = sROI.copy()    #   copy to mark up for display
    Scnt  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
    # sort left to right
    print ' input is ms {} mx {} tval {}  count {} '\
          .format(ms,mx,tx, len(cnt))
    x,y,w,h = boundsBlob(cnt)    #    outer bounds of blob area
    print (x,y,w,h)
    tl = (x-10,y-10) ; br = ( x  +  w+10, y+ h+10)       #  10 for more room
    cv2.rectangle(img2,(tl),(br),(255,255,255),1)         # white rectangle
    #cvs( db, img2, ' sROI')
    lx = []
    for i, f in enumerate (Scnt):       # scan left to right sorted contours             
       
        print ' blob {}'.format(i),
        # compare blob to our file of tempate blobs 
        ret,n = evaluate(f,db)
        if ret:
            print 'evaluate returns {}, number {}'.format(ret,n)
            cv2.drawContours(img2,[f],0,(0,255,0),1)    # draw after capture
            cmask = cmask -cmask
            cv2.drawContours(cmask,[f],0,(255,255,255),1)
            lx.append(n)
            #cvs(0,cmask,'cmask')
            cvs(db,img2,'evaluate')
            
    return lx                   # list of numbers in the panel

if  __name__ == '__main__':
    global db     
    db = 1
    fx = 'pics\sc_sample_terran_1087_267_67_94.png'
    
    h,w,ROI = Part(fx,db)      #  ROI   region of interest
    ROI = cv2.imread('input.png')
    cvs(db, ROI, 'input')
    listx = evalGame(ROI,db)
    print 'eval game returns',listx    
    cvd()

    



