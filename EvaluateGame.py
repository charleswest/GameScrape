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
    or    n == 0 and area < 400 ):
        return(False,0)
    elif  dist >  .15:
        return(True,eval2(cnt1,db))
    else:
        return(True,n)
       



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
       
        if db: print ' blob {}'.format(i)
        # compare blob to our file of tempate blobs
        #tmpeval(f,db)                      #  explore alternate evaluation
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
def eval2(cnt1,db):
    ''' match the incomming contour against the set of binary patterns.
        replace files by binary patterns with a high low equal value
        start with just upper/lower to try and weed out 5 and 2
'''
    
    ''' we need to zero base the x's  and y's in   cnt1 '''
    x1 = tuple(cnt1[cnt1[:,:,0].argmin()][0])    # leftmost
    y1 = tuple(cnt1[cnt1[:,:,1].argmin()][0])    #  topmost 
    for c in cnt1:
        c[0][0] = c[0][0] + 1 - x1[0]
        c[0][1] = c[0][1] + 1 - y1[1]
 #       print c[0][0]                      move blob to pos 1,1
        numb= [
               (111, 0),
                (66, 1),
               (225, 2),
               (186, 3),
               (168, 5),
               (108, 6),
                (78, 7),
               (114, 8),
               (213, 9)
              ]    
 #   print 'cnt1', cnt1
    h=25; w=35
    imgB = np.zeros((h,w,3), np.uint8)              # empty black window
    cv2.drawContours(imgB,[cnt1],0,(255,255,255),1)
    cv2.rectangle(imgB,(0,0),(w,h/2),(0,0,0),-1)    # solid fill rectangle
    xn = np.sum(imgB)/255
    mx,n = min(numb,key= lambda xx: abs(xx[0] -xn)  )
    if db: print  'BW sum {} looks like {}'.format(xn,n)
    imgB = cv2.resize(imgB,(4*w,4*h))
    cvs(db,imgB,'half black')
    return(n)

if  __name__ == '__main__':
    global db     
    db = 1
    fx = 'pics\sc_sample_terran_1087_267_67_94.png'
    h,w,ROI = Part(fx,db)
    
    #  ROI   region of interest
    ROI = cv2.imread('input.png')    #   uses the last image from mainloop
    cvs(db, ROI, 'input')
    listx = evalGame(ROI,db)
    print 'eval game returns',listx    
    cvd()

    



