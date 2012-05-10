#!/usr/bin/python

import sys
sys.path.append('/usr/libsvm/python')
from svmutil import *

f_train = 'training_set' if len(sys.argv) < 3 else sys.argv[1]
f_test = 'testing_set' if len(sys.argv) < 3 else sys.argv[2]
f_write = 'libsvm_result' if len(sys.argv) < 4 else sys.argv[3]

y_train, x_train = svm_read_problem(f_train)
m = svm_train(y_train, x_train, '-c 4')
y_test, x_test = svm_read_problem(f_test)
p_label, p_acc, p_val = svm_predict(y_test, x_test, m)

f = open(f_write, 'w')
for i in range(len(y_test)):
    f.write("%s %s %f\n" % (y_test[i], p_label[i], p_val[i][0]))