#!/usr/bin/python

import sys
sys.path.append('/usr/libsvm/python')
from svmutil import *

f_train = 'test-graph-2011-07-04' if len(sys.argv) < 3 else sys.argv[1]
f_test = 'test-graph-2011-08-04' if len(sys.argv) < 3 else sys.argv[2]

y_train, x_train = svm_read_problem(f_train)
m = svm_train(y, x, '-c 4')
y_test, x_test = svm_read_problem(f_test)
p_label, p_acc, p_val = svm_predict(y_test, x_test, m)