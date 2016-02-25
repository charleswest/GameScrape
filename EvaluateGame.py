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
    #closeUp(cnt1,db)
    path = ("blobs\\*.png" )                
    files = glob.glob(path)
    rn = [] 
    for xn,f in enumerate(files):                
        n   = int(f[-5:-4])                    #get n from filename       
        img = cv2.imread(f,0)                  # read a digit 
        h,w = img.shape[:2]       
        ret, contours,hierarchy = cv2.findContours(img,2,1)
        cnt2 = contours[0]

        dist = cv2.matchShapes(cnt1,cnt2,1,0.0)
        area = cv2.contourArea(cnt1)
        if db: print 'dist from number {} is {} area is {}'.format( n, round(dist,5),area)
        rn.append( (dist,n) )     #  list of result from matchShapes 
        
    #  pick the one with the lowest score
    (dist,n) = min(rn, key = lambda (dist,n): dist )         #   minimum distence  
    if db: print 'rn is ',round(dist,5), n, 'area' ,area
    #  if the best one was close enough filter further based on number and area
    #  
    if (  dist >  .35          #.1:
    or    n == 4 and (area < 200 or area > 310)
    or    n == 8 and (area < 400 )      
    or    n == 0 and  area < 400  ):
        return(False,0)

    else:
        return(True,n)

def evalRegion(ROI,db):
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
       
        if db: print ' blob {}'.format(i)
        # compare blob to our file of template blobs
        #tmpeval(f,db)                      #  explore alternate evaluation
        ret,n = evaluate(f,db)
        if ret:          
            cv2.drawContours(img2,[f],0,(0,255,0),1)    # draw after capture
            cmask = cmask -cmask
            cv2.drawContours(cmask,[f],0,(255,255,255),1)
            lx.append(n)
            if db: print '>>>evaluate {}   <<<'.format(lx)
            #cvs(0,cmask,'cmask')
            x= cvs(db,img2,'evaluate')
            if x in [1,2,3,4,5,6,7,8,9,0 ] : capture(f,x)
            
    nn = 0 ; lx.reverse()   
    for j, xin in  enumerate(lx):
        nn = nn + xin * 10**(j)
    return  nn     #                  as normal decimal number
            
#    return lx                   # list of numbers in the panel
def evalGame(fx,db):
    lx = []
    h,w,r1,r2,r3,r4 = Part(fx,db)
    for ROI in [r1,r2,r3,r4]:
        cv2.imwrite('input.png',ROI)
        img = np.zeros((48,100,3), np.uint8)          # empty black window
        cvs(0,img,'input')
        cvs(db, ROI, 'input')
        lx.append(evalRegion(ROI,db))
    return tuple(lx)

if  __name__ == '__main__':
    global db     
    db = 1
    fx = 'pics\sc_sample_terran_302_1312_168_188.png'
    listx = evalGame(fx,db)
    print 'eval game returns',listx   
    
    #  ROI   region of interest
#    ROI = cv2.imread('input.png')    #   uses the last image from mainloop
    
    cvd()

    



