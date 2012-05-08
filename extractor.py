#!/usr/bin/python

from features_util import *
from sys import argv

method = 's' if len(argv) < 2 else argv[1]
test_snapshot = 'test-graph-2011-07-04' if len(argv) < 4 else argv[2]
result_snapshot = 'test-graph-2011-08-04' if len(argv) < 4 else argv[3]

f_test = Feature_Extractor(test_snapshot)
f_result = Feature_Extractor(result_snapshot)

follows = f_test.get_follow_only_edges()
results = f_result.get_results(follows)

i = 0
for (p1, p2) in follows:
    if results[i]:
        print "+1" if method == 's' else "1",
    else:
        print "-1" if method == 's' else '0',
    
    #Common Neighbors
    num_common_neighbors = len(list(f_test.get_common_friends(p1, p2)))
    print '1:%s' % str(num_common_neighbors) if method == 's'else str(num_common_neighbors),
    
    print
    i += 1