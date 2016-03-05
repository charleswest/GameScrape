f = open("digits.txt", "r")
# omit empty lines and lines containing only whitespace
lines = [line for line in f if line.strip()]
f.close()
lines.sort()
print 'n,       S,     LR,      TB,   LR==S,   TB==S'
for xx in lines:
    n, S, LR, TB = xx.split()
    print '{}\t{}\t{}\t{}\t'.format(n, S, LR, TB),
    print (LR < 40 ), '\t', (n > 5), n
