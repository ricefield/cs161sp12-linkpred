#!/usr/bin/python

from sys import stdin, stdout, argv

POSITIVES = ['+1', '1']
NEGATIVES = ['-1', '0']
    
def main():
    lines = stdin.readlines()
    lines = [line.strip().split() for line in lines]
    true_pos = 0
    true_neg = 0
    false_pos = 0
    false_neg = 0
    for line in lines:
        pred = line[0]
        real = line[1]
        if real in POSITIVES and pred in POSITIVES:
            true_pos += 1
        elif real in POSITIVES and pred in NEGATIVES:
            true_neg += 1
        elif real in NEGATIVES and pred in POSITIVES:
            false_pos += 1
        elif real in NEGATIVES and pred in NEGATIVES:
            false_neg += 1
    
    acc = float(true_pos)/(true_pos + true_neg)
    print "Predicted %f of actual follow-backs." % acc
    acc2 = float(true_pos)/(true_pos + false_pos)
    print "%f of predicted follow-backs were correct." % acc2
    acc3 = float(true_pos + false_neg)/(true_pos + false_pos + true_neg + false_neg)
    print "%f of all predictions were accurate." % acc3
    
main()
