#!/usr/bin/python

from sys import stdin, stdout, argv

class Link():
    def __init__(self, input):
        if len(input) == 0:
            raise Exception('Link does not take empty arg')
        vals = input.split(',', 2)
        if len(vals) < 2 or len(vals) > 3:
            raise Exception('Link must take 2- or 3-value string')
        self.start = vals[0]
        self.end = vals[1]
        if len(vals) == 3:
            self.prob = float(vals[2])
        else:
            self.prob = 1.0
    
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        return self.start != other.start or self.end != other.end

    def __str__(self):
        print "(" + self.start + "->" + self.end + ")"
            
def testLink():
    l1 = Link('a,b')
    l2 = Link('c,d')
    assert l1 != l2
    l3 = Link('b,a')
    assert l1 != l3
    l4 = Link('a,b,0.5')
    assert l1 == l4

POSITIVES = ['+1', '1']
NEGATIVES = ['-1', '0']
    
def main():
    lines = stdin.readlines()
    lines = [line.strip() for line in lines]
    
    sep = lines.index('')
    newEdges = lines[:sep]
    newEdges = [Link(edge) for edge in newEdges if edge != '']
    predEdges = lines[sep+1:]
    predEdges = [Link(edge) for edge in predEdges if edge != '']
    
    numNewEdges = len(newEdges)
    count = 0
    for edge in newEdges:
        if edge in predEdges:
            count += 1
    ratioFound = float(count)/numNewEdges
    print "Found %f percent of new edges." % (ratioFound*100)
    
    numPredEdges = len(predEdges)
    count = 0
    for edge in predEdges:
        if edge in newEdges:
            count += 1
    ratioAccurate = float(count)/numPredEdges
    print "%f percent of predictions are accurate." % (ratioAccurate*100)

testLink()    
main()
