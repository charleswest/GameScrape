'''
This routine takes the imput full size photo and segments it .  As interesting numbers are outlined in green they can be captured and labeled with any number key or skipped
with any other key.  q will terminate the program.
More than one photo is required to capture all numbers.  Captured digits should be inspected and moved to the blobs sub directory
'''
import numpy as np
import cv2
from cwUtils import cvd, cvs, erode, dilate
from AnalyseDigits import findNumbers
from DigitStat import identifyN, parm
import warnings

global db

def Part(  fx,db):
    ''' partition the image and return the ROI '''
    img = cv2.imread(fx)
    h,w = img.shape[:2]
    #print 'image h {} w {}'.format(h,w)
    y1  = .02 * h  ; y2 = int(.04 * h)
    x1  = int (.79  * w)  ; x2 = int(w)

    
    ROI =  img[ 26:39,    1510:1900 ].copy()
     
     
##    ROI =  img[ y1:y2,        1510:1585  ].copy()   # 177
##    ROI1 = img[ y1:y2,        1650:1725  ].copy()   # 438
##    ROI2 = img[ y1:y2,        1775:1900  ].copy()   # 101
##    ROI3 = img[ y1:y2,        1820:1900  ].copy()   # 129
    
    return(h,w,ROI)

def capture(f,lb,mask):
    global db
    ''' write out the ith blob to a file'''
    x,y,w,h = cv2.boundingRect(f)
#    blb =  mask[y-1:y+h+1, x-1:x+w+1].copy()     #   capture the thresholded img
    blb =  mask[y:y+h, x:x+w].copy()
    #    with a 1 pxl border
    cvs(1,blb,'blbx')
   

    parm.lst  = identifyN(blb,lb,db)
    print parm.lst
    n = parm.lst[1]
   
    cv2.imwrite('aMLblob{}.png'.format(lb),blb)
    print 'number is {} w {} h {} identify {}'.format(lb,w,h,n)

    blbx = cv2.resize(blb,(4*w,4*h))
    cvs(1,blbx,'capture')



if  __name__ == '__main__':
    print __doc__
    global db     
    db = 0
    fil = "pics\sc_sample_terran_177_438_101_129.png"
    fil = "pics\sc_sample_terran_1452_835_95_148.png"
    #fil = "pics\sc_sample_terran_1087_267_67_94.png"
    #fil = 'input.png'
    h,w,ROI = Part(fil,db)
    h,w = ROI.shape[:2]
    sROI =   cv2.resize(ROI,(3*w,3*h))        #    this may not be a good idea    
    sROI = erode(sROI,1)
    cxcopy = sROI.copy()    #   copy to mark up for display                                         # but we did it in CaptureDigits so .. .
    cmask,cnt,hier = findNumbers(sROI,db)    # in
    Scon  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))

    for i, f in enumerate (Scon):                
        area = cv2.contourArea(f)
        print ' blob {}  {}  area {} '.format(i,hier[0][i],area  )
        cv2.drawContours(cxcopy,[f],0,(0,255,255),2)    # draw after capture
        if area > 250 and area < 1900:            
            key = cvs(1,cxcopy,'cxcopy')
            print ' '
            if key in [1,2,3,4,5,6,7,8,9,0 ] : capture(f,key,cmask)        
    cv2.imwrite('\pics\blobs.png',cut)
    cvd()
    print('end gam1')
    
    
