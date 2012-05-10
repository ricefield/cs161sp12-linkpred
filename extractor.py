#!/usr/bin/python

from features_util import *
from sys import argv

method = 's' if len(argv) < 2 else argv[1]
test_snapshot = 'graph-2011-07-04' if len(argv) < 4 else argv[2]
result_snapshot = 'graph-2011-08-04' if len(argv) < 4 else argv[3]
output_name = 'output' if len(argv) < 5 else argv[4]
DEBUG = False if len(argv) < 6 else (argv[5] == "-v")   

f_test = Feature_Extractor(test_snapshot, DEBUG)
f_result = Feature_Extractor(result_snapshot, DEBUG)

if DEBUG:
    print "finding follows"
follows = f_test.get_follow_only_edges()
if DEBUG:
    print "%d follows tracked" % len(follows)
    print "finding results"
complete = (result_snapshot == 'graph-2011-07-11')
results = f_result.get_results(follows, complete)

count = 0
mid = len(follows)/2
fs = open(output_name + '_train_s', 'w')
fp = open(output_name + '_train_p', 'w')
try:
    for (p1, p2) in follows:

        if count == mid:
            fs.close()
            fp.close()
            fs = open(output_name + '_test_s', 'w')
            fp = open(output_name + '_test_p', 'w')
        
        #Result
        if results[count]:
            #print "+1" if method == 's' else "1",
            fs.write("+1")
            fp.write("1")
        else:
            #print "-1" if method == 's' else "0",
            fs.write("-1")
            fp.write("0")
        
        feature = 1
        
        #Common Neighbors
        num_common_neighbors = len(list(f_test.get_common_friends(p1, p2)))
        #print '%d:%d' % (feature, num_common_neighbors) if method == 's' else str(num_common_neighbors),
        fs.write(' %d:%d' % (feature, num_common_neighbors))
        fp.write(str(num_common_neighbors))
        feature += 1
        
        #Jacaard
        for mut_neighbor_type in range(9):
            for neighbor_type in range(3):
                j_val = f_test.get_jaccard(p1, p2, neighbor_type, mut_neighbor_type)
                #print '%d:%f' % (feature, j_val) if method == 's' else '%f' % j_val,
                fs.write(' %d:%f' % (feature, j_val))
                fp.write(' %f' % j_val)
                feature += 1
        
        #Adamic-Adar
        for mut_neighbor_type in range(9):
            for neighbor_type in range(3):
                aa_val = f_test.get_adamic(p1, p2, neighbor_type, mut_neighbor_type)
                #print '%d:%f' % (feature, aa_val) if method == 's' else '%f' % aa_val,
                fs.write(' %d:%f' % (feature, aa_val))
                fp.write(' %f' % aa_val)
                feature += 1
        
        #Preferential Attachment
        for neighbor_type in range(3):
            pref = f_test.get_pref_attachment(p1, p2, neighbor_type)
            #print ' %d:%d' % (feature, pref) if method == 's' else '%d' % pref,
            fs.write(' %d:%d' % (feature, pref))
            fp.write(' %d' % pref)
            feature += 1
        
        #print
        fs.write('\n')
        fp.write('\n')
        
        count += 1
        if DEBUG:
            print count,
except:
    print "ERROR"
fs.close()
fp.close()
