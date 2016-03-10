# -*- coding: utf-8 -*-
import numpy as np
import cv2
import sys
global db
from cwUtils import cvs, cvd , erode, dilate

db = True
def stdSize(imgx,typ):
    h,w = imgx.shape[:2]   #   h = rows,  w = cols
    if 1:
        nw = 800
    else:
        nw = 400
   
    nh =   h * (float(nw) / float(w))  
    print 'stdSize height {} typ {} nw {}'.format( nh, typ, nw)
    imgy =  cv2.resize(imgx, ( nw, int (nh) )  )    # maintain aspect ratio
    
    return imgy.copy()

def  analBlob(grp):
    # x, y, w, h    given the following x,y pairs
#     [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
    x,y = grp[0][0][0]
    mxy = y
    print x,y
    for  cn in grp:
        for blb in cn:
                #print y,
                cx,cy  = blb[0] 
                 
                if cx  < x: x = cx                #  find least x
                if cx  > x: w = cx - x
                
                if cy < y: y = cy                #  find max y
                if cy > mxy: mxy = cy
                #print 'y and mxy', y,mxy
    h = mxy - y
    return( x,y,w,h)
def analBlob2(grpx):
    for grp in grpx: 
        leftmost =   tuple(grp[grp[:,:,0].argmin()][0])
        rightmost =  tuple(grp[grp[:,:,0].argmax()][0])
        topmost =    tuple(grp[grp[:,:,1].argmin()][0])
        bottommost = tuple(grp[grp[:,:,1].argmax()][0])
    (x,y) = leftmost,topmost
    print x, y , 'analblob2'
##    w = rightmost - x
##    h = bottommost -y
    return(x,y )
def  findBlobs(imx,ms,mx,erd,db,tval=127):
  
    Erd = erd
    Drd = int(Erd/2) 
    print 'This is find blobs  1.0 ms {} mx {} erd {} drd {}'.format( ms, mx , Erd ,Drd)
    imgray = cv2.cvtColor(imx,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,tval,255,0)
    thresh = erode(thresh,Erd)
    thresh = dilate(thresh,Drd)
    #print 'db findBlobs' , db
    cvs(db,thresh)
    cmask = thresh.copy()
    im3,cnt, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #  note lamda is expression for leftmost extreme of the contour
    scon  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
 
    rvl = []
    for con in scon:
       area = cv2.contourArea(con)
       if db: print  area,
       
       cnt_len = cv2.arcLength(con, True)                          
       cntp = cv2.approxPolyDP(con, 0.02*cnt_len, True)
 #      print len(cntp)  #    look for suitable contours
       x,y,w,h = cv2.boundingRect(con)
       asp = abs(  w - h  )
       if db: print 'abs|w-h| {}  w {} h {} '.format(asp,w,h)
       if len(cntp) > 3  \
          and asp > .1 \
          and  area > ms and area < mx:
            rvl.append(con)
            cv2.drawContours(imx,[con], 0, (0,255,255), 1)    # yellow
        
       else:
          cv2.drawContours(imx,[con], 0, (0,0,255), 1)       #  red
          
       if db:cvs(db,imx,t=0)
    return (rvl,cmask)
   
if __name__ == '__main__':
    db = False
    print 'funny ', db
 
    tst = 'fat'
    imgx = cv2.imread ('input.png')
    #imgx = cv2.imread(fn)
    img =  imgx  #stdSize(imgx,tst)   #cv2.resize(imgx, (1040,410))
    srt = img.copy()
    h,w = img.shape[:2]  
 
    #cvs(db,img)
    ms =  20;    mx = 150;  erd =0; tx=20
    (cnt,cmask) =  findBlobs( img,ms,mx,erd,db,tx) # will modify img to show cnt
    cnt  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
    print ' input is {} width {} height {} ms {} mx {} tval {}   '\
          .format(tst,w, h,ms,mx,tx)
    print len(cnt) ,'blobs were found shape is list'
##    x,y,w,h = cv2.boundingRect(cnt)     #  needs single image or array
##    print 'boundingRec {} {} {} {}'.format( x,y,w,h)
    a,b = analBlob2(cnt)
    print a,b, 'analBlob2'
    x,y, w,h = analBlob(cnt)
    
    
    tl = (x-10,y-10) ; br = ( x  +  w+10, y+ h+10)       #  10 for more room
    cv2.rectangle(cmask,(tl),(br),(255,255,255),5)       # white rectangle


##    print 'min x {}'.format(minx)
    for i, f in enumerate (cnt):
        #print '{} cnt {}'.format(i,f)
        cv2.drawContours(img,[f],0,(255,0,0),1)
        #print 'contour array f[0] ',  f[0] ,
        x,y,w,h = cv2.boundingRect(f)
        a =  cv2.contourArea(f)
        asp = round(abs( 1.00 - float(w)/float(h) ),2)
        print 'x {}  y {}\tw {}\th {}\ta {}\tasp {} '.format( x, y , w, h,a,asp)
        
        cv2.rectangle(img,(tl),(br),(255,255,255),5)
        cvs(1,img,'img 3',3)
 
    cvd()
