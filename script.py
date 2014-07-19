import os
import sys

if len(sys.argv) !=(2+1):
	print '1: tree depth'
	print '2: cores'
	exit(-1)
tree_depth = sys.argv[1]
smooth_N = '3'
cores = sys.argv[2]
for setting in ['set_4_2012','set_5','set_6','set_1_2013','set_2_2012','set_3_2012']:
	cmd = 'python2.7 run.py %s %s %s  %s' % (tree_depth,smooth_N,cores,setting)
	print '-' * 50
	print cmd
	print '-' * 50
	os.system(cmd)



