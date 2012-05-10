#!/usr/bin/python

from random import random, randint

fs1 = open("fake_data_train_s", "w")
fp1 = open("fake_data_train_p", "w")
fs2 = open("fake_data_test_s", "w")
fp2 = open("fake_data_test_p", "w")

data_s = "+1"
data_p = "1"
for i in range(50):
    rand_val = random()
    data_s += " %d:%f" % (i+1, rand_val)
    data_p += " %f" % rand_val
data_s += "\n"
data_p += "\n"
for i in range(1000):
    fs1.write(data_s)
    fp1.write(data_p)
    fs2.write(data_s)
    fp2.write(data_p)
    
data_s = "-1"
data_p = "0"
for i in range(50):
    rand_val = random()
    data_s += " %d:%f" % (i+1, rand_val)
    data_p += " %f" % rand_val
data_s += "\n"
data_p += "\n"
for i in range(1000):
    fs1.write(data_s)
    fp1.write(data_p)
    fs2.write(data_s)
    fp2.write(data_p)
    
fs1.close()
fp1.close()
fs2.close()
fp2.close()