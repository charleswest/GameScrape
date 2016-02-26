x = [1,2,3,4,5,'s',6,7]
y = x.index('s')
print x,  y
s1 = x[:y]
s2 = x[y+1:]
print s1   ,'      ', s2
