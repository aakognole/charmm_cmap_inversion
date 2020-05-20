#------------------------------------------------------------
# This script converts CHARMM L-aa CMAP to D-aa CMAP
# by akognole May 2020
#------------------------------------------------------------

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sys import argv

try:
    inp = str(argv[1])
except IndexError:
    print('Usage: python cmap_inversion <input_file> <output_file>')
    exit()

try:
    out = str(argv[2])
except:
    out = 'inverted_'+inp
    
# Convert CHARMM format into numpy array
cmap = open(inp, 'r')
L = []
i = 0
for x in cmap:
    if x.startswith("!"):
        i = 0
        D1 = []
    else:
        i = i + 1
        l = x.split()
        for j in range(len(l)):
            D1.append((l[j]))
        if i == 5:
            L.append(D1)

L = np.array(L)
np.savetxt('./nparray/'+inp, L, fmt="%s")

#step to invert
temp = np.flipud(L)
temp = np.fliplr(temp)
temp = np.roll(temp,shift=1,axis=0)
D = np.roll(temp,shift=1,axis=1)

np.savetxt('./nparray/'+out, D, fmt="%s")

# Convert back to charmm format
f = open(out, 'w')
phi = -180
for i in range(24):
    f.write('!phi = %d\n' % (phi))
    f.write('%8s %8s %8s %8s %8s\n' % (D[i,0],D[i,1],D[i,2],D[i,3],D[i,4])) 
    f.write('%8s %8s %8s %8s %8s\n' % (D[i,5],D[i,6],D[i,7],D[i,8],D[i,9]))
    f.write('%8s %8s %8s %8s %8s\n' % (D[i,10],D[i,11],D[i,12],D[i,13],D[i,14]))
    f.write('%8s %8s %8s %8s %8s\n' % (D[i,15],D[i,16],D[i,17],D[i,18],D[i,19]))
    f.write('%8s %8s %8s %8s\n' % (D[i,20],D[i,21],D[i,22],D[i,23]))
    f.write('\n')
    phi = phi + 15
f.close()
    
