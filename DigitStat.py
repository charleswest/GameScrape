''' load and analyse numbers '''
import numpy as np
import cv2
from cwUtils import cvd, cvs, erode, dilate
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

if  __name__ == '__main__':
    print __doc__
    digits, labels =     cwload_digits_lst("blobs\\aML*.png" )
    for d , lb in zip(digits,labels):
        print d.shape , lb , np.sum(d) / 255
        # w < 30 is a 1
