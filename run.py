#!/usr/bin/env python2.7
import pandas as pd
import sys
from rf import *
import ycchen_features as yft
import sheep_features as sft
import math
import numpy as np

def smooth(data,smooth_N,mean):
    print 'mean: ' + str(mean)
    data['teacher_ratio_before_2010414_no_process'] = (data['teacher_hit_before_2010414_no_process'] + smooth_N * mean) / (data['teacher_count_before_2010414_no_process'] + smooth_N)
    return data

def fill_missing_zero(data,features):
	print 'fill the missing'
	for col in features:
		data[col][pd.isnull(data[col])] = 0
	return data
	
def gen_submission(ans,id,output):
	submit = dict()
	submit['projectid'] = id
	submit['is_exciting'] = ans
	submitData = pd.DataFrame(data = submit)
	submitData.to_csv(output,index = False,cols = ['projectid','is_exciting'])

def info(tree_depth,smooth_N,core,setting):
	print 'tree_depth: ' + str(tree_depth)
	print 'smooth_N: ' + str(smooth_N)
	print 'core: ' + str(core)
	print 'setting: ' + setting
	
def gen_importance(ret , name , depth,smooth_N):
	print 'generate importance.csv'
	temp = dict()
	temp ['importance'] = ret['importance']
	temp ['features'] = features
	temp = pd.DataFrame(temp)
	temp = temp.sort('importance',ascending = [0])
	temp.to_csv(out_base + 'importance_' + name + '_' + str(depth) +'_smooth_' + str(smooth_N) + '_smoothGreat_3.csv', index = False)	
	
if __name__ == '__main__':
	if len(sys.argv) != (4+1) :
		print 'Usage:'
		print '1:tree_depth'
		print '2:smooth_N'
		print '3:core'
		print '4:setting (TA1/TA2/TA1_skip)'	
		exit(-1)
	
	tree_depth = int(sys.argv[1])
	smooth_N = int(sys.argv[2])
	core = int(sys.argv[3])
	setting = sys.argv[4]
	info(tree_depth,smooth_N,core,setting)
	
	
	
	###file location setting
	base = '/home/kdd2/kdd2014/generated_features/merge/f037/'
	train_file = base + 'ext_2013_train_merge.csv'
	test_file = base + 'ext_2013_valid_merge.csv'
	
	### internal file setting
	loc_int_train = base + setting + '_train_merge.csv'
	loc_int_valid = base + setting + '_valid_merge.csv'

	### start date setting
	if setting == 'set_1_2013':
		start_date = '2013-01-01'
	elif ((setting == 'set_2_2012') or (setting == 'set_3_2012') or (setting == 'set_4_2012')):
		start_date = '2012-01-01'
	elif (setting == 'set_5') or (setting == 'set_6'):
		start_date = '2010-04-14'
	print start_date
	
	
	if setting == 'set_2':
		retrain_flag = True
	else:
		retrain_flag = False
		
	out_base = '/home/kdd2/kdd2014/submit/s035exp/' + setting + '/' 	
	postfix = str(tree_depth) + '_smooth_' + str(smooth_N) + '_smoothGreat_3'
	valid_output = out_base + 'valid_' + postfix + '.csv'
	print valid_output
	test_output = out_base + 'test_' + postfix + '.csv'
	print test_output
	
	print 'current train file : ' + train_file
	print 'current test file : ' + test_file
	
	#whether to retrain
	print 'process the data...'
		
	'''
		Features Part
	'''
	###setting features and parameter
	features = []
	features.extend(['res_avg_price_fill'])
	features.extend(['students_reached'])
	features.extend(['num_of_resources', 'resource_price'])
	features.extend(['essay_length_char'])
	features.extend(['total_price_excluding_optional_support', 'total_price_including_optional_support'])
	features.extend(yft.projects_expand)
	
	great_prop_features = 'great_prop_prediction_' + setting + '_smoothGreat_3'
	features.extend([great_prop_features])
	features.extend(sft.teacher_features_no_process)
		
	
	
	'''
		Data Part
	'''
	### Read the data
	print 'Read the data...'
	data = pd.read_csv(train_file)
	date = data['date_posted']
	fulfill = data['fulfillment_labor_materials']
	data = data[ (date >= start_date) & ((fulfill == 30) | (fulfill == 35))]
	print 'length of data: ' + str(len(data))
	print 'done!'
	
    ###fill the missing of students_reached
	print 'fill missing...'
	data = fill_missing_zero(data,features)
	print 'done!!!'
	
	###   make the ans column
	data['ans'] = 0
	data['ans'][data['is_exciting'] == 't'] = 1
	mean = np.mean(data['teacher_ratio_before_2010414_no_process'][data['teacher_count_before_2010414_no_process']!=0])
	data = smooth(data, smooth_N, mean)

	###split the data and check the performance
	
	print 'split the data ...'
	### deal with train
	train = pd.read_csv(loc_int_train)
	date = train['date_posted']
	fulfill = train['fulfillment_labor_materials']
	train = train[ (date >= start_date) & ((fulfill == 30) | (fulfill == 35))]
	
	###fill the missing of students_reached
	train = fill_missing_zero(train,features)
	
	###   make the ans column
	train['ans'] = 0
	train['ans'][train['is_exciting'] == 't'] = 1
	train = smooth(train, smooth_N,mean)
	print 'length of train: ' + str(len(train))
	
	###deal with valid
	valid = pd.read_csv(loc_int_valid)
	valid = fill_missing_zero(valid,features)
	valid['ans'] = 0
	valid['ans'][valid['is_exciting'] == 't'] = 1
	valid = smooth (valid,smooth_N,mean)
	print 'length of valid: ' + str(len(valid))
	
	print 'training ...'
	print 'Tree depth is:' + str(tree_depth)
	params = {'n_estimators':300, 'max_depth':tree_depth , 'min_samples_split':3 , 'max_features':None,'random_state':1,'n_jobs':core}
	ret = RFC(train,valid,features,params)
	AUC = ret['valid_auc']
	print 'AUC is : %f' % AUC
	
	gen_submission( ret['valid_predict'] , valid['projectid'] , valid_output)
	
	log = open(out_base + 'valid_AUC_' + postfix + '.txt','w')
	log.write(str(AUC))	
	log.close()
	
	gen_importance(ret,'valid',tree_depth,smooth_N)
	
	### retrain
	if retrain_flag:
		###setting features and parameter
		features.remove(great_prop_features)
		great_prop_features = 'great_prop_prediction_ext_smoothGreat_3'
		features.extend([great_prop_features])
		### Generate the testing set

		test = pd.read_csv(test_file)
		
		### fill the missing
		test = fill_missing_zero(test,features)
		test = smooth(test,smooth_N,mean)
		###Retraining
		print 'retraining ... '
		ret = RFC(data,test,features,params)
		ans = ret['valid_predict']
		
		###Generate the submission
		print 'generate the submission ...'
		
		gen_submission( ret['valid_predict'] , test['projectid'] , test_output)
		
		### generate the importance.csv
		gen_importance(ret,'test',tree_depth,smooth_N)
	
	