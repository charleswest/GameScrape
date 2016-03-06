import numpy as np
def printsort():
    f = open("digits.txt", "r")
    # omit empty lines and lines containing only whitespace
    lines = [line for line in f if line.strip()]
    f.close()
    #lines.sort()
      

    dts = np.zeros((len(lines),13),dtype='int32' )       # rows by columns
    for i,xx in enumerate(lines):
        [lb,n, t0,L,R,T,B , S, LR,TB ] = map(int, xx.split())
       
        dts[i] = [lb,  n,  t0   , L,     S,   LR,  TB, t0<512, L<385,S<150,LR<150,TB<90,TB==S]
    head =   '''[  lb n t0  L   S,  LR, TB t0<512,  S<150, TB<90
                                     L<385  LR<150  TB==S] '''
    sx =   ( dts[:,11],  dts[:,10] ,  dts[:,9],  dts[:,8],  dts[:,7],  dts[:,6]           )
    sx =   (dts[:,10],dts[:,9], dts[:,8], dts[:,7], dts[:,6]  ,  dts[:,0]           )

    srt  = dts   [  np.lexsort(  sx        )    ]
    ix = 0
    print head
    for row in srt:
        if row[1] == ix:
            print  row
        else:
            ix = row[1]
            print ' '
            if ix == 5: print head
            print row
    print head
if  __name__ == '__main__':
    printsort()
