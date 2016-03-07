import numpy as np
def printsort():
    f = open("digits.txt", "r")
    # omit empty lines and lines containing only whitespace
    lines = [line for line in f if line.strip()]
    
    f.close()
    #lines.sort()
    print 'lenghtlines', len(lines)  

    dts = np.zeros((len(lines),12),dtype='int32' )       # rows by columns
    for i,xx in enumerate(lines):
       # print xx
        [ lb,n,t0,L,R,T,B,S,LR,TB,M3 ] = map(int, xx.split())
       
        dts[i] = ([lb,  n, t0,L,  R,  B,  T,  M3,  LR,  S,   TB, abs(S-TB)<5])
        
    head =   '''[ lb   n, t0, L,  R   B   T   M3  LR  S   TB  abs(S-TB)<5]      
                                                          '''

   # sx =   (  dts[:,12]  ,dts[:,11],  dts[:,10]           )
    sx =   (  dts[:,1] , dts[:,0]  )
    srt  = dts   [  np.lexsort( sx      )    ]
    ix = 0
    nx = 0; correct = 0; fkl = []; fkd = 0
    print head
    for row in srt:
        if  row[0] == row[1]:
            correct += 1
        else:
            fkd +=1
            fkl.append((row[0],row[1]))
        if row[nx] == ix:
            print  row
        else:
            ix = row[nx]            
            if ix == ix:
                print head
            else:
               print ' '
               pass
            print row
    print head
    print '{}  percent correct {} out of {}'.format(correct*100/len(srt),correct,len(srt))
    return fkl
if  __name__ == '__main__':
    prb = printsort()
    print ' problems are', prb
