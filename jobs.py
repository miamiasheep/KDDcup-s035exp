import os
'''
1: tree depth
2: smooth_N
3: smooth_N_ref
4: cores
'''

cores = 10
for d in [6,7,8,10,12]:
	cmd = 'python2.7 script.py %d %d' % (d,cores)
	print cmd
	os.system(cmd)