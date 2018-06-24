#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string

models = {}
for c in string.ascii_lowercase:
    try:
        t = {chr(i + ord('a')): float(line.strip())
             for i, line in enumerate(open(f'models/{c}.model'))}
        models[c] = t
    except IOError:
        pass


def jpname_prob(name):
    """
    >>> jpname_prob('Tarou Tanaka')
    0.1946955087272778
    >>> jpname_prob('Andrew Ng')
    0.04630919707172066
    """
    names = name.lower().split()
    prob = 0.0
    nbigram = 0
    for name in names:
        for a1, a2 in zip(name, name[1:]):
            nbigram += 1
            try:
                prob += models[a1][a2]
            except KeyError:
                prob -= 0.2
    return prob / nbigram


def names_prob(names):
    """
    >>> names_prob(['Tarou Tanaka', 'Ichiro Sato'])
    0.20652925216626383
    """
    probs = [jpname_prob(name) for name in names]
    return sum(probs) / len(probs)
