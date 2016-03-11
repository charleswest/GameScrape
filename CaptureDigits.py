'''
This routine takes the imput full size photo and segments it .  As interesting numbers are outlined in green they can be captured and labeled with any number key or skipped
with any other key.  q will terminate the program.
More than one photo is required to capture all numbers.  Captured digits should be inspected and moved to the blobs sub directory
'''
import numpy as np
import cv2
from cwUtils import cvd, cvs, erode, dilate
from DigitStat import identifyN, parm
import warnings

global db
def findNumbers(cut,db):
    ''' take the ROI and look for posible numbers. Convert to gray, blur the region,
    erode and dilate the picture to improve resolution.  Now, find the contours and
    return the contours, our working image and the hierarchy of contours'''
    
    cxcopy = cut.copy()
    cvs(db,cxcopy,'cxcopy',3)
    if db: print 'cxcopy.shape', cxcopy.shape
    ms = 100;   mx = 1500; erd = 0; tx = 127
    img2 = cut.copy()    #   copy to mark up for display
    gray = cv2.cvtColor(cut,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    #cvs(db,blur,'blur image')

    ret,thresh = cv2.threshold(blur,127,255,cv2.THRESH_BINARY) 
##    thresh = erode(thresh,1)   
##    thresh = dilate(thresh,2)
    if db: cvs(db, thresh,'threshold',3)
    img2 =  thresh.copy()               # maybe std size here
    jnk,cnt, hier= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
      #and hier[0][i][3] == -1
    if db: print '{} contours found'.format(len(cnt))
    cnt = [ cn     for i,cn in enumerate(cnt) if hier[0][i][3] == -1 ]

    
    ''' if right most cnt is < 280 re threshold on 40 and splice masks'''    
    scon  =   max(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmax()][0]))
    x,y,w,h = cv2.boundingRect(scon[-1])
    print 'red checked', x
    if x < 280 :
        
        # try again with low tx value
        ret,thresh2 = cv2.threshold(blur,40,255,cv2.THRESH_BINARY)
        # now splice the two thresholds
        left = img2[:,0:280] ; right = thresh2[:,280:]
        combo = np.hstack((left,right))
        
        if db: cvs(db, combo,' red threshold',3)
        img2 =  combo.copy()
        jnk,cnt, hier= cv2.findContours(combo,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
       
        print 'red numbers exit'
        
    return(img2,cnt,hier)
                    



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
    cv2.imwrite('ROI.png',ROI)
    return(h,w,ROI)

def capture(f,lb,mask,db):
     
    ''' write out the ith blob to a file'''
    x,y,w,h = cv2.boundingRect(f)
#    blb =  mask[y-1:y+h+1, x-1:x+w+1].copy()     #   capture the thresholded img
    blb =  mask[y:y+h, x:x+w].copy()
    #    with a 1 pxl border
    cvs(1,blb,'blbx')
   

##    parm.lst  = identifyN(blb,lb,db)
##    print parm.lst
##    n = parm.lst[1]
   
    cv2.imwrite('aMLblob{}.png'.format(lb),blb)
 #   print 'number is {} w {} h {} identify {}'.format(lb,w,h,n)

     
    cvs(1,blb ,'capture',4)



if  __name__ == '__main__':
    print __doc__
    global db     
    db = 1
    fil = "pics\sc_sample_terran_177_438_101_129.png"
    fil = "pics\sc_sample_terran_69_148_27_38.png"
    fil = "pics\sc_sample_zerg_99_20_19_18_red.png"
    #fil = 'input.png'
    h,w,sROI = Part(fil,db)
    h,w = sROI.shape[:2]
 #   sROI =   cv2.resize(ROI,(3*w,3*h))        #    this may not be a good idea    
 #   sROI = erode(sROI,1)
    cxcopy = sROI.copy()    #   copy to mark up for display                                         # but we did it in CaptureDigits so .. .
    cmask,cnt,hier = findNumbers(sROI,db)    # ,in
    Scon  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))

    for i, f in enumerate (Scon):
        x,y,w,h = cv2.boundingRect(f)
        area = cv2.contourArea(f)
        
       
        if area > 25  and area < 1900:
            cv2.drawContours(cxcopy,[f],0,(0,255,255),2)    # draw after capture
            print ' blob  {} x {}  {}  area {} '.format(i,x,hier[0][i],area  )
            key = cvs(1,cxcopy,'cxcopy',3)         
            if key in [1,2,3,4,5,6,7,8,9,0 ] : capture(f,key,cmask,db)
            
 
##            blb =  cmask[y:y+h, x:x+w].copy()
##            parm.lst  = identifyN(blb,key,db)
##            print parm.lst
##            n = parm.lst[1]
##            lb = parm.lst[0]
            #print 'number is {} w {} h {} identify {}'.format(lb,w,h,n)
            
    cvd()
    print('end gam1')
    
    
