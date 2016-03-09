''' load and analyse numbers  DigitStat'''
import numpy as np
import cv2
from cwUtils import cvd, cvs, erode, dilate
import itertools as it
class parm():
    lstN = 12
    head =   '''  lb, n  t0,  L,  R,  T  ,B  ,S,  LR, TB, M3 Mv3 '''
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
    d = p.copy()
    h,w = d.shape
    im2 = d.copy()
    t0 = np.sum(im2) / 255

    d[:, w/2:] = 0        # same as bitwise and
    L = np.sum(d)/255

    d = im2.copy()
    d[:, :w/2] = 0
    R = np.sum(d)/255

    d = im2.copy()         #  upper half
    d[ h/2:, : ] = 0
    T = np.sum(d)/255

    d = im2.copy()         #  lower half
    d[ :h/2, : ] = 0          # zero upper half
    B = np.sum(d)/255

    d = im2.copy()         #  middle horiz third
    d[   :h/3, : ] = 0        #    - upper 1/3
    d[ 2*h/3:, : ] = 0        #    - lower 1/3
    M3 = np.sum(d)/255

    d = im2.copy()         #  middle vert third
    d[   :w/3, : ] = 0        #    - upper 1/3
    d[ 2*w/3:, : ] = 0        #    - lower 1/3
    Mv3 = np.sum(d)/255

    # statistics
    S =  ( max(L,R,T,B) - min(L,R,T,B)) 
    LR =  abs(L-R) 
    TB =  abs(T-B)
    ASTB = abs(S-TB)<6
    n = 99; pl = []
    # 80 96 54 2   7 3 1 
    if (t0> 750   and M3>270 and TB < 17    
                                           ):   n = 8
    elif (t0> 730
       and abs(M3-166)<10                  ):   n = 0
    
    elif  (abs(M3-280)<10 and LR < 38      ):   n = 6
    
    elif  (abs(M3-280)<10                  ):   n = 9
    elif  (abs(M3-215)<10 and LR < 30      ):   n = 5
    elif  (abs(Mv3-310)<10                 ):   n = 4
    
    elif  (abs(M3-240)<20                  ):   n = 2
    elif  (abs(M3-170)<20                  ):   n = 3
    elif   ( L>191                         ):   n = 7
    else:                                       n = 1
    lb = int(lb)
    parm.lst = [lb,n,t0,L,R,T,B,S,LR,TB,M3,Mv3 ]
    return parm.lst 
def prtTable(digits,labels):
    
    dts = np.zeros((10,parm.lstN),dtype='int32' )   
    for d , lb in zip(digits,labels):      
        parm.lst = identifyN(d,lb,0)
        #print 'parm lst',parm.lst
        dts[lb] = parm.lst
    print parm.head 
    print dts
if  __name__ == '__main__':
    print __doc__
    digits, labels =     cwload_digits_lst("blobs\\aML*.png" )
    prtTable(digits,labels)

         
        

