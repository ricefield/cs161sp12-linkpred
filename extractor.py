#!/usr/bin/python

from features_util import *
from sys import argv

method = 's' if len(argv) < 2 else argv[1]
test_snapshot = 'graph-2011-07-04' if len(argv) < 4 else argv[2]
result_snapshot = 'graph-2011-08-04' if len(argv) < 4 else argv[3]
output_name = 'output' if len(argv) < 5 else argv[4]
DEBUG = False if len(argv) < 6 else (argv[5] == "-v")   

f_test = Feature_Extractor(test_snapshot)
f_result = Feature_Extractor(result_snapshot)

if DEBUG:
    print "finding follows"
follows = f_test.get_follow_only_edges()
if DEBUG:
    print "finding results"
results = f_result.get_results(follows)

count = 0
mid = len(follows)/2
f = open(output_name + '_train_' + method, 'w')
try:
    for (p1, p2) in follows:

        if count == mid:
            f.close()
            f = open(output_name + '_test_' + method, 'w')
        
        #Result
        if results[count]:
            #print "+1" if method == 's' else "1",
            f.write("+1" if method == 's' else "1")
        else:
            #print "-1" if method == 's' else "0",
            f.write("-1" if method == 's' else "0")
        
        feature = 1
        
        #Common Neighbors
        num_common_neighbors = len(list(f_test.get_common_friends(p1, p2)))
        #print '%d:%d' % (feature, num_common_neighbors) if method == 's' else str(num_common_neighbors),
        f.write(' %d:%d' % (feature, num_common_neighbors) if method == 's' else str(num_common_neighbors))
        feature += 1
        
        #Jacaard
        for mut_neighbor_type in range(9):
            for neighbor_type in range(3):
                j_val = f_test.get_jaccard(p1, p2, neighbor_type, mut_neighbor_type)
                #print '%d:%f' % (feature, j_val) if method == 's' else '%f' % j_val,
                f.write(' %d:%f' % (feature, j_val) if method == 's' else '%f' % j_val)
                feature += 1
        
        #Adamic-Adar
        for mut_neighbor_type in range(9):
            for neighbor_type in range(3):
                aa_val = f_test.get_adamic(p1, p2, neighbor_type, mut_neighbor_type)
                #print '%d:%f' % (feature, aa_val) if method == 's' else '%f' % aa_val,
                f.write(' %d:%f' % (feature, aa_val) if method == 's' else '%f' % aa_val)
                feature += 1
        
        #Preferential Attachment
        for neighbor_type in range(3):
            pref = f_test.get_pref_attachment(p1, p2, neighbor_type)
            #print ' %d:%d' % (feature, pref) if method == 's' else '%d' % pref,
            f.write(' %d:%d' % (feature, pref) if method == 's' else '%d' % pref)
            feature += 1
        
        #print
        f.write('\n')
        
        count += 1
        if DEBUG:
            print count
except:
    print "ERROR"
f.close()
