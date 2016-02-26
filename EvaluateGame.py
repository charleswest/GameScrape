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
from CaptureDigits import Part, capture
import warnings 
print __doc__

def evaluate( cnt1,db):
    ''' match the incomming contour against the set of digits we have stored in
        blobs.  '''
 #   global db
    #closeUp(cnt1,db)
    path = ("blobs\\*.png" )                
    files = glob.glob(path)
    rn = [] ; ssx = False
    for xn,f in enumerate(files):                
        n   = (f[-5:-4])                    #get n from filename       
        img = cv2.imread(f,0)                  # read a digit 
        h,w = img.shape[:2]       
        ret, contours,hierarchy = cv2.findContours(img,2,1)
        cnt2 = contours[0]

        dist = cv2.matchShapes(cnt1,cnt2,1,0.0)
        area = cv2.contourArea(cnt2)
        area1 = cv2.contourArea(cnt1)
        if db and dist < .5:
            print 'dist {} {} is {} area is {}'.format(f[6:], n, round(dist,5),area)
        rn.append( (dist,n) )     #  list of result from matchShapes 
        
    #  pick the one with the lowest score
    (dist,n) = min(rn, key = lambda (dist,n): dist )         #   minimum distence  
    if db: print 'rn is ',round(dist,5), n, 'area' ,area
    #  if the best one was close enough filter further based on number and area
    #  
    if (  dist >  .5    #.35          #.1:
    or    n == '4' and (area1 < 200 or area1 > 310)
    or    n == '8' and (area1 < 400 )
    or    n == 'S' and ssx == True
    or    n == '0' and  area1 < 400  ):
        return(False,0)
    else:
        if n == 'S' : ssx = True       #  switch for only one of these
        return(True,n)

def evalRegion(ROI,db):
    ''' we obtain the ROI region of interest  from Part or as input from the
        last screen processed by Maintest.   We look for blob in the ROI and
        evaluate them by matching to our recorded set of captured digits.
    '''
    #global db
    h,w = ROI.shape[:2]
    sROI =     ROI       #                                            
    ms = 80;   mx = 550; erd = 0; tx = 127
    # ms minimum size
    # erd erosion dilation -- leave this at zero
    # tx the threshold for the binary mask 
    (cnt,cmask) =  findBlobs(sROI,ms,mx,erd,0,tx) # will modify img to show cnt
    img2 = sROI.copy()    #   copy to mark up for display
    if db: print ' input is ms {} mx {} tval {}  count {} '\
          .format(ms,mx,tx, len(cnt))
    x,y,w,h = boundsBlob(cnt)    #    outer bounds of blob area
    if db: print (x,y,w,h)
    tl = (x-10,y-10) ; br = ( x  +  w+10, y+ h+10)       #  10 for more room
    cv2.rectangle(img2,(tl),(br),(255,255,255),1)         # white rectangle
    #cvs( db, cmask, ' sROI')
    lx = []
    for i, f in enumerate (cnt):       # scan left to right sorted contours             
       
        if db: print ' blob {}'.format(i)
        # compare blob to our file of template blobs
        #tmpeval(f,db)                      #  explore alternate evaluation
        ret,n = evaluate(f,db)
        if ret: #  n could be S  for slash                               
            lx.append(n)
        if db:
            print '< {} >>>evaluate {}   <<<'.format(n, lx)
            #cvs(0,cmask,'cmask')
            cv2.drawContours(cmask,[f],0,(255,255,255),1)
            cv2.drawContours( img2,[f],0,(255,255,0)  ,1)  
            x= cvs(db,img2,'evaluate')
            if x in [1,2,3,4,5,6,7,8,9,0   ] : capture(f,x,cmask,db)     
            
    return lx       # one or two  lists of numbers in the panel

def nlx(lx):
    ''' return normal decimal number  from input list'''
       
    nn = 0 ; lx.reverse()   
    for j, xin in  enumerate(lx):
        nn = nn + int( xin) * 10**(j)
    return  nn     #                  as

def evalGame(fx,db):
    lx = []
    h,w,r1,r2,r3,r4 = Part(fx,db)
    for ROI in [r1,r2,r3]:
        h,w = ROI.shape[:2]
        R2x = cv2.resize(ROI,(2*w,2*h)) 
        cv2.imwrite('input.png',ROI)
        img = np.zeros((48,100,3), np.uint8)          # empty black window
        cvs(0,img,'input')
        cvs(db, R2x, 'input')
        tlx = evalRegion(R2x,db)
        if 'S' in tlx :
            inx = tlx.index('S')
            s1x = tlx[:inx]
            s2x = tlx[inx+1:]          
            #print 'eg lx{} slx {} s2x {}'.format( lx, s1x,s2x )        
            lx.append( (nlx(s1x) ))
            lx.append( (nlx(s2x) ))         
        else:        
            lx.append( (nlx(tlx) ))       
    return lx

if  __name__ == '__main__':
    global db     
    db = 1
    fx = 'pics\sc_sample_terran_114_112_22_38.png'
    listx = evalGame(fx,db)
    print 'eval game returns',listx   
    cvd()

    



