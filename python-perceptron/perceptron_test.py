# Copyright (c) 2009 Leif Johnson <leif@leifjohnson.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''Command line tests for the basic Perceptron library.

The data for the tests comes from :
http://www.ncrg.aston.ac.uk/GTM/3PhaseData.html
'''

import numpy

import perceptron


EVENT_SIZE = 12
OUTCOME_SIZE = 3
DEGREES = (1, 3, 5)
GAMMAS = (0.001, 0.01, 0.1, 1)
BEAM_WIDTHS = (1, 10, 100, 1000)


def learners():
    kwargs = dict(event_size=EVENT_SIZE, outcome_size=OUTCOME_SIZE)
    for klass in ('Perceptron', 'AveragedPerceptron'):
        factory = getattr(perceptron, klass)
        yield (klass, '  vanilla   ', factory(**kwargs))
        for d in DEGREES:
            yield (klass,
                   'polynomial-%d' % d,
                   factory(kernel=perceptron.polynomial_kernel(d), **kwargs))
        for g in GAMMAS:
            yield (klass,
                   'radial-%.3f' % g,
                   factory(kernel=perceptron.radial_basis_kernel(g), **kwargs))
    for b in BEAM_WIDTHS:
        yield ('SparseAveragedPerceptron',
               'beam-%d' % b,
               perceptron.SparseAveragedPerceptron(beam_width=b, **kwargs))


def _parse(filename):
    '''Parse events and outcomes from a data file.'''
    with open(filename) as handle:
        for line in handle:
            try:
                fields = map(float, line.strip().split())

                assert len(fields) == 1 + EVENT_SIZE

                outcome = int(fields[0]) - 1
                assert 0 <= outcome < OUTCOME_SIZE

                yield outcome, numpy.array(fields[1:])
            except:
                pass


def _features(event):
    '''Extract binary features from a continuous event.'''
    for i, value in enumerate(event):
        for threshold in (0.001, 0.01, 0.1, 1, 10, 100, 1000):
            if value > threshold:
                yield '%d>%f' % (i, threshold)
            if value < threshold:
                yield '%d<%f' % (i, threshold)
            if value > -threshold:
                yield '%d>%f' % (i, -threshold)
            if value < -threshold:
                yield '%d<%f' % (i, -threshold)


def train(learner):
    '''Train a learner on a set of sample data.'''
    for outcome, event in _parse('data/flow-train.txt'):
        features = event
        if isinstance(learner, perceptron.SparseAveragedPerceptron):
            features = set(_features(event))
        learner.learn(features, outcome)


def test(learner):
    '''Test a learner on a randomly generated set of data.'''
    correct = [0] * OUTCOME_SIZE
    j = 0
    for j, (outcome, event) in enumerate(_parse('data/flow-test.txt')):
        features = event
        if isinstance(learner, perceptron.SparseAveragedPerceptron):
            features = set(_features(event))
        pred, _ = learner.classify(features)
        if pred == outcome:
            correct[outcome] += 1
    return correct, j


if __name__ == '__main__':
    for klass, flavor, learner in learners():
        train(learner)
        correct, count = test(learner)
        print '%s - %s - accuracy %.2f, correct per class %s' % (
            klass, flavor, 100.0 * sum(correct) / count, correct)
