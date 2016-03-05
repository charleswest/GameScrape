''' load and analyse numbers  DigitStat'''
import numpy as np
import cv2
from cwUtils import cvd, cvs, erode, dilate
import itertools as it
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
#   cv2.imshow('training set', mosaic(10, digits[:]))
#   print 'training set labels', labels
    return(digits,labels)

def FndN(d,lb=0,db=0):
    h,w = d.shape
    im2 = d.copy()
    t0 = np.sum(im2) / 255

    d[:, w/2:] = 0        # same as bitwise and
    t1 = np.sum(d)/255

    d = im2.copy()
    d[:, :w/2] = 0
    t2 = np.sum(d)/255

    d = im2.copy()         #  upper half
    d[ h/2:, : ] = 0
    t3 = np.sum(d)/255

    d = im2.copy()         #  lower half
    d[ :h/2, : ] = 0
    t4 = np.sum(d)/255
    t4S =  ( max(t1,t2,t3,t4) - min(t1,t2,t3,t4)) 
    t6LR =  abs(t1-t2) 
    t7TB =  abs(t3-t4)
    n = 99; pl = []
 
    if t4S < 30       and t7TB < 20:         n = 8
    elif t6LR < 40    and t7TB > 100:        n = 5
    elif t6LR < 20    and t7TB > 50:         n = 2
    elif t6LR < 15    and t7TB > 20:         n = 0
   
    elif t6LR < 50    and t7TB > 30:         n = 9
    elif t6LR < 50    and t7TB <= 30:        n = 6
    elif t6LR < 88    and t7TB >= 130:       n = 7
    elif t6LR < 110   and t7TB >= 50:        n = 4   
    elif t6LR >= 100  and t7TB < 50:         n = 3
    else:                                    n = 1
    if db :print  ('{}\t{}\t{}\t{}\t{}'
            .format(lb,n,t4S,t6LR,t7TB))
    return(lb,n,t4S,t6LR,t7TB)

if  __name__ == '__main__':
    print __doc__
    digits, labels =     cwload_digits_lst("blobs\\aML*.png" )
    print 'lb\tn \tt4S\t6LR\t7TB '
    rtn = []
    for d , lb in zip(digits,labels):
        lb,n,t4S,t6LR,t7TB = FndN(d,lb,0)
        rtn.append((lb,n,t4S,t6LR,t7TB))

    rtn = sorted(rtn, key = lambda (lb,n,t4S,t6LR,t7TB):t6LR)
    for (lb,n,t4S,t6LR,t7TB) in rtn:
        print  ('{}\t{}\t{}\t{}\t{}'
            .format(lb,n,t4S,t6LR,t7TB))
    cvd()
        # w < 30 is a 1
