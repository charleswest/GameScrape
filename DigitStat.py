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
    L = np.sum(d)/255

    d = im2.copy()
    d[:, :w/2] = 0
    t2 = np.sum(d)/255

    d = im2.copy()         #  upper half
    d[ h/2:, : ] = 0
    t3 = np.sum(d)/255

    d = im2.copy()         #  lower half
    d[ :h/2, : ] = 0
    t4 = np.sum(d)/255
    S =  ( max(L,t2,t3,t4) - min(L,t2,t3,t4)) 
    LR =  abs(L-t2) 
    TB =  abs(t3-t4)
    n = 99; pl = []
     
    if t0> 512 and L >385 and S< 150 and TB <90  and abs(S-TB)<5:   n = 8
    elif LR < 40    and TB > 100:        n = 5
    elif LR < 20    and TB > 50:         n = 2
    elif t0> 512 and L <385 and S< 150 and TB <90 and TB == S:    n = 0
   
    elif LR < 50    and TB > 30:         n = 9
    elif LR < 50    and TB <= 30:        n = 6
    elif LR < 88    and TB >= 130:       n = 7
    elif LR < 110   and TB >= 50:        n = 4   
    elif LR >= 100  and TB < 50:         n = 3
    else:                                n = 1
    lb = int(lb)
    return[lb,n,t0,L,t2,t3,t4,S,LR,TB ]

if  __name__ == '__main__':
    print __doc__
    digits, labels =     cwload_digits_lst("blobs\\aML*.png" )

    dts = np.zeros((10,13),dtype='int32' )   
    for d , lb in zip(digits,labels):      
        lb,n,t0,L,t2,t3,t4,S,LR,TB = FndN(d,lb,0)
        dts[lb] = [lb,  n,  t0 , L, S,LR,TB, t0<512, L<385,S<150,LR<150,TB<90,TB==S]
        
    head =   '''[  lb   n,t0, L,   S,  LR, TB t0<512,  S<150, TB<90      
                                  L<385  LR<150  TB==S]'''
    print head 
    print dts
         
        

