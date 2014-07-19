
resources_related = ['num_of_resources', 'resource_price', 'num_of_quantity']
essay_length = ['essay_length_char', 'essay_length_word']
price_diff_ratio = ['price_diff_ratio_2013']

project_counts = ['month_projects_count', 'daily_projects_count']


'''teacher features '''
teacher_features_no_process = ['teacher_hit_before_2010414_no_process','teacher_ratio_before_2010414_no_process']
teacher_features_no_process_int_1 = ['teacher_count_before_2010414_no_process_int_1','teacher_hit_before_2010414_no_process_int_1','teacher_ratio_before_2010414_no_process_int_1']
teacher_features_no_process_mean = ['teacher_count_before_2010414_no_process_mean','teacher_hit_before_2010414_no_process_mean','teacher_ratio_before_2010414_no_process_mean']
teacher_features_no_process_int_1_mean = ['teacher_count_before_2010414_no_process_int_1_mean','teacher_hit_before_2010414_no_process_int_1_mean','teacher_ratio_before_2010414_no_process_int_1_mean']

teacher_features_no_test_count = ['teacher_count_before_2010414_no_test_count','teacher_hit_before_2010414_no_test_count','teacher_ratio_before_2010414_no_test_count']
teacher_features_no_test_count_int_1 = ['teacher_count_before_2010414_no_test_count_int_1','teacher_hit_before_2010414_no_test_count_int_1','teacher_ratio_before_2010414_no_test_count_int_1']

teacher_features_test_ratio_stable = ['teacher_count_before_2010414_test_ratio_stable','teacher_hit_before_2010414_test_ratio_stable','teacher_ratio_before_2010414_test_ratio_stable']
teacher_features_test_ratio_stable_int_1 = ['teacher_count_before_2010414_test_ratio_stable_int_1','teacher_hit_before_2010414_test_ratio_stable_int_1','teacher_ratio_before_2010414_test_ratio_stable_int_1']

'''referred_count '''
ref_count = ['teacher_refer_total_2010414','teacher_refer_ratio_2010414']
ref_count_int_1 = ['teacher_refer_total_2010414_int_1','teacher_refer_ratio_2010414_int_1']



# The above is the features of 0.61331 version #

# New Idea!
# essay_word_count = ['essay_length_word']
# num_of_quantity = ['num_of_quantity']

# features that will decrease the AUC on validation
geometry = ['school_latitude', 'school_longitude']

# features that will decrease the AUC on leaderboard
poverty = ['poverty_level']
