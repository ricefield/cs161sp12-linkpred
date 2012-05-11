#!/usr/bin/python

from sys import stdin, stdout, argv

POSITIVES = ['+1', '1.0', '1']
NEGATIVES = ['-1', '-1.0', '0']
    
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
    
    soundness = float(true_pos)/(true_pos + true_neg)
    print "%f\tpercent of actual follow-backs predicted." % soundness*100
    completeness = float(true_pos)/(true_pos + false_pos)
    print "%f\tpercent of predicted follow-backs were correct." % completeness*100
    accuracy = float(true_pos + false_neg)/(true_pos + false_pos + true_neg + false_neg)
    print "%f\tpercent of all predictions were accurate." % accuracy*100
    
main()
