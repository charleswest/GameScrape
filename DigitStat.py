''' load and analyse numbers  DigitStat'''
import numpy as np
import cv2
from cwUtils import cvd, cvs, erode, dilate
import itertools as it
class parm():
    lstN = 12
    head =   '''  lb, n  t0,  L,  R,  T  ,B  S   LR  TB, M3 Mv3 '''
    ahd  =   '''  lb n t0  L R  T  B  S  LR TB M3 Mv3 '''

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
       # img = erode(img,1)
        print( 'im  shape {} {}'.format( fn ,img.shape)  )
        #img = np.floaT2(cv2.resize(img,(40,35) ))
        dl.append(img)
    digits = dl    #np.array(dl)
    labels = np.array(lbl)
#   cv2.imshow('training set', mosaic(10, digits[:]))
#   print 'training set labels', labels
    return(digits,labels)

def identifyN(p,lb=0,db=0):
    ''' identify creates digit descriptor vectors by counting the contours under a set of
    masks applied to the digit being examined.  Masks are applied by setting the non mask
    area of the image to zero, black.
    '''
    
    def pxCount(d, msk ):
        jk,cnt4d, hier  = cv2.findContours(d,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        m = len(cnt4d)
        
        if m: msk.append(m)
        else: msk.append(0)
        return(msk)
       
    d = np.zeros_like(p)
    d = p.copy()
    h,w = d.shape
    im2 = d.copy()
    t0 = np.sum(im2) / 255
    cvs(db,d,'digit  ',5)

    d[:, w/2:] = 0        # same as bitwise and
    L = np.sum(d)/255
    cvs(db,d,'digit  ',5)
    msk = [] 
    msk = pxCount(d,msk)
    
    d = im2.copy()
    d[:, :w/2] = 0
    R = np.sum(d)/255
    cvs(db,d,'digit  ',5)
    msk = pxCount(d,msk)

    d = im2.copy()         #  upper half
    d[ h/2:, : ] = 0
    T = np.sum(d)/255
    cvs(db,d,'digit  ',5)
    msk = pxCount(d,msk)

    d = im2.copy()         #  lower half
    d[ :h/2, : ] = 0          # zero upper half
    B = np.sum(d)/255
    cvs(db,d,'digit  ',5)
    msk = pxCount(d,msk)
    
    d = im2.copy()         #  middle horiz third
    d[   :h/3, : ] = 0        #    - upper 1/3
    d[ 2*h/3:, : ] = 0        #    - lower 1/3
    M3 = np.sum(d)/255
    cvs(db,d,'digit h Mid 1/3',5)
    msk = pxCount(d,msk)
    

    d = im2.copy()         #  middle vert third
    d[ :,  :w/3  ] = 0        #    - left 1/3
    d[ :, 2*w/3:  ] = 0        #    - right 1/3
    Mv3 = np.sum(d)/255
    cvs(db,d,'digit  v Mid3',5)
    mm = pxCount(d,msk )
    
    if db: print 'final mask for {} {}'.format(lb,mm)
    
    # statistics
    S =  ( max(L,R,T,B) - min(L,R,T,B)) 
    LR =  abs(L-R) 
    TB =  abs(T-B)
    #  identify the input
    if   (t0 > 75
               # L  R  T  B  h  v        #  left right top bottom horiz vertical
    and  mm ==  [1, 1, 1, 1, 2, 2]): n = 0
    elif mm ==  [1, 1, 1, 1, 2, 1]: n = 1
    elif mm ==  [0, 1, 1, 1, 2, 1]: n = 1   # hack for bad threshold
    elif mm ==  [1, 1, 1, 1, 1, 1] and h == 11 : n = 1 
    elif mm ==  [2, 2, 1, 1, 2, 3]: n = 2
    elif mm ==  [1, 2, 1, 1, 1, 3] :n = 2   # noisy 2
    elif mm ==  [3, 1, 1, 1, 1, 3]: n = 3
    elif mm ==  [3, 1, 1, 1, 2, 3]: n = 3   # noisy 3 
    elif mm ==  [1, 1, 1, 1, 2, 2]: n = 4
    elif mm ==  [1, 1, 1, 1, 1, 2]: n = 4   # noisy 4
    elif mm ==  [2, 2, 1, 2, 1, 3]: n = 5
    elif mm ==  [1, 2, 1, 2, 1, 3]: n = 6
    elif mm ==  [2, 1, 1, 1, 1, 2]: n = 7
    elif mm ==  [1, 1, 2, 2, 1, 3]: n = 8
    elif mm ==  [2, 1, 1, 1, 1, 3]: n = 9
    elif mm ==  [1, 1, 1, 2, 1, 3]: n = 9   # noisy 9
    else :n = -1
    
    lb = int(lb)
    parm.lst = [lb,n,t0,L,R,T,B,S,LR,TB,M3,Mv3 ]
    d = d - d
    return parm.lst

def prtTable(digits,labels):
    db = 1
    dts = np.zeros((10,parm.lstN),dtype='int32' )   
    for d , lb in zip(digits,labels):
        #print '     ',parm.head 
##        if lb in range(10):
         parm.lst = identifyN(d,lb,db)
##            print '     ',parm.head  
##            print 'parm   ',parm.lst,'\n'
##            cvs(1,d,'digit',4)
         dts[lb] = parm.lst
            
    print dts
if  __name__ == '__main__':
    print __doc__
    digits, labels =     cwload_digits_lst("blobs\\aML*.png" )
    prtTable(digits,labels)
    cvd()

         
        

