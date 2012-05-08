from features_util import *
from sys import argv

method = 's'
str1 = 'test-graph-2011-07-04'
str2 = 'test-graph-2011-08-04'
f_test = Feature_Extractor(str1)
f_result = Feature_Extractor(str2)
follows = f_test.get_follow_only_edges()
results = f_result.get_results(follows)
i = 0
for (p1, p2) in follows:
    if results[i]:
        print "+1" if method == 's' else "1",
    else:
        print "-1" if method == 's' else '0',
    
    #Common Neighbors
    num_common_neighbors = len(list(f_test.get_common_neighbors(p1, p2)))
    print '1:%s' % str(num_common_neighbors) if method == 's'else str(num_common_neighbors),
    
    print
    i += 1