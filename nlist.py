''' explore ways of finding the best match '''
numb= [
               (111, 0),
               (225, 2),
               (186, 3),
               (168, 5),
               (108, 6),
                (78, 7),
               (114, 8),
               (213, 9)
              ]
#def near(t): return abs(numb[][0] - t) <3
   
##for xx in numb:
##    print xx , xx[0], xx[1],
##    print abs(xx[0] - 112) < 3
    
t = 110    
def near(xx): return abs(xx[0] -t )

print sorted(numb,key=near)
print min(numb,key=near)
