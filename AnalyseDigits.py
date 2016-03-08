'''
This routine takes the imput full size photo and segments it .  As interesting numbers
are outlined in green they can be captured and labeled with any number key or skipped
with any non numeric key.  q will terminate the program.  m will perform a match of the
current highlighted number with the full set of previously captured numbers.

More than one photo is required to capture all numbers.  Captured digits should be
inspected and moved to the blobs sub directory.
'''
import numpy as np
import cv2
from cwUtils import cvd, cvs, erode, dilate
from DigitStat import identifyN ,parm  
import warnings
 

def Part(  fx,db):
    ''' partition the image and return the ROI '''
    img = cv2.imread(fx)
    h,w = img.shape[:2]
    #print 'image h {} w {}'.format(h,w)
    y1  = .02 * h  ; y2 = int(.04 * h)          # initial guess at region
    x1  = int (.79  * w)  ; x2 = int(w)
    ROI =  img[ 26:39,    1510:1900 ].copy()    #  specific pixel positons 
    return(h,w,ROI)

def capture(f,j,mask):
    ''' input i contour and ROI and N.   The image of n is saved '''
    
    ''' write out the ith blob to a file'''
    x,y,w,h = cv2.boundingRect(f)
#    blb =  mask[y-1:y+h+1, x-1:x+w+1].copy()     #   capture the thresholded img
    blb =  mask[y:y+h, x:x+w].copy()
    #    with a 1 pxl border
   # x = cvs(db,blb,'blbx')
    cv2.imwrite('aMLblob{}.png'.format(j),blb)
    print 'number is ' , j
    for m in cv2.HuMoments(cv2.moments(blb)).flatten():
        print m
    blbx = cv2.resize(blb,(4*w,4*h))
    cvs(db,blbx,'capture')
    
def cwload_digits_lst(fn):
    ''' load a set of saved numbers into a list for comparison to possible numbers
        returned by find numbers '''
    import os
    import glob
 #   print('loading {} ...'.format(fn))
    path = fn               
    files = glob.glob(path)
    dl = []; lbl = []
    for f in files:
        fn = int((f[-5:-4]))
        lbl.append(fn)                    #get n label from filename       
        img = cv2.imread(f,0)
        img = erode(img,1)
        #print( 'im  shape {} {}'.format( fn ,img.shape)  )
        #img = np.float32(cv2.resize(img,(40,35) ))
        dl.append(img)
    digits = dl    #np.array(dl)
    labels = np.array(lbl)
#    cv2.imshow('training set', mosaic(10, digits[:]))
 #   print 'training set labels', labels
    return(digits,labels)

def findNumbers(cut,db):
    ''' take the ROI and look for posible numbers. Convert to gray, blur the region,
    erode and dilate the picture to improve resolution.  Now, find the contours and
    return the contours, our working image and the hierarchy of contours'''
    
    cxcopy = cut.copy()
    cvs(db,cxcopy,'cxcopy')
    ms = 100;   mx = 1500; erd = 0; tx = 127
    img2 = cut.copy()    #   copy to mark up for display
    gray = cv2.cvtColor(cut,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    #cvs(db,blur,'blur image')

    ret,thresh = cv2.threshold(blur,127,255,cv2.THRESH_BINARY) 
    thresh = erode(thresh,1)   
    thresh = dilate(thresh,2)
    cvs(db, thresh,'threshold')
    img2 =  thresh.copy()               # maybe std size here
    jnk,cnt, hier= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
      #and hier[0][i][3] == -1
    rcnt = [ cn     for i,cn in enumerate(cnt) if hier[0][i][3] == -1 ]
    return(img2,rcnt,hier)

def xdebug(c1,c2):
    'display imput params to match shapes'
    print 'xdebug'
    m1 = cv2.HuMoments(cv2.moments(c1)).flatten()
    m2 = cv2.HuMoments(cv2.moments(c2)).flatten()
    mm1 = cv2.moments(c1)
    mm2 = cv2.moments(c2)
##    for m in mm1:
##        print m, '\t\t', mm1[m],'\t\t\t\t', mm2[m]
    print '  Hu moments '
    for mx, my in zip( m1,m2):
        print mx, '\t\t', my
    print ' '
def  cmatch(f,cnt2,possible,im):
##    m1 = cv2.HuMoments(cv2.moments(c1)).flatten()
##    m2 = cv2.HuMoments(cv2.moments(c2)).flatten()
    
    return(99)
def evalGame(ROI):
    h,w = ROI.shape[:2]
    cut = cv2.resize(ROI,(3*w,3*h))
    cut = erode(cut,1)
    cxcopy = cut.copy()
    ## load the saved digits list
    digits, labels =     cwload_digits_lst("blobs\\aML*.png" )
    img,cnt,hier = findNumbers(cut,db)
    print hier.shape, len(cnt)
    print 'next, prev, 1st c. , parent\n',hier
    lx = []
    for i, f in enumerate (cnt):     #   for each possible n in the input                
        area = cv2.contourArea(f)
        
        cv2.drawContours(cxcopy,[f],0,(0,255,255),2)    # draw yellow
        x,y,w,h = cv2.boundingRect(f)
        print ' blob {}  {}  area {} x {}'.format(i,hier[0][i],area ,x )
        if area > 250 :         #  no parent
            possible = img[y:y+h, x:x+w].copy()
            cvs(db,possible,'possible')
            key = cvs(db,cxcopy,'cxcopy')        #key is keypress from cvs
            if key in [1,2,3,4,5,6,7,8,9,0 ] : capture(f,key,img)     
  #          elif True: # key == ord('m') - 48 :
            n = -1; mdist = 999; rnl = []

            parm.lst = identifyN(possible,0,1)
            n = parm.lst[1]
            print 'match returns {}  '.format(n )
            key = cvs(db,possible,'match')
            if key in [1,2,3,4,5,6,7,8,9,0 ] : capture(f,key,img)
            elif key == ord('z') -48: xdebug(f,cnt2)
            else: lx.append((x,n))
    lx  =  sorted(lx,key = lambda (x,n):x )
    lx = [b for (a,b) in lx]
    return  lx              
            
if  __name__ == '__main__':
    print __doc__
    global db     
    db = 1
    fil = "pics\sc_sample_terran_177_438_101_129.png"
    fil = "pics\sc_sample_terran_1452_835_95_148.png"
    #fil = "pics\sc_sample_terran_1087_267_67_94.png"
    fil = "pics\sc2_sample_game_screen.png"
    #fil = 'input.png'
 
    h,w,ROI = Part(fil,db)
    #cvs(db,c1)
    lx = evalGame(ROI )
    print lx
                    
   
    cvd()
    print('end gam1')
    
    
