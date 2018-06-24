#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
import itertools


def gen_model(given):
    N = 2
    with open("names.num") as names:
        names = [[int(alph) for alph in name.strip().split(" ")] for name in names]
    nalphs = 26
    allalphs = list(range(nalphs))
    ngram_count = [[0.0] * nalphs for _ in range(N)]

    # Count all unigrams and bigrams
    for alphs_seq in names:
        for a1 in alphs_seq:
            ngram_count[0][a1] += 1
        for a1, a2 in zip(alphs_seq, alphs_seq[1:]):
            if a1 == given:
                ngram_count[1][a2] += 1

    # Compute parameters
    totals = [sum(counts) for counts in ngram_count]
    nss = [[float(sum(v == r for v in counts)) + 10e-10 for r in range(1, 6)]
           for counts in ngram_count]
    Ys = [nss[i][0] / (nss[i][0] + 2 * nss[i][1]) for i in range(N)]
    Dss = [[0.0] + [j - (j + 1) * Ys[i] * nss[i][j] / nss[i][j - 1]
                    for j in range(1, 5)]
           for i in range(N)]
    def D_index(n, w):
        return min(int(ngram_count[n][w]), 4)

    gammas = [(Dss[i][1] * sum(v == 1 for v in ngram_count[i]) +
               Dss[i][2] * sum(v == 2 for v in ngram_count[i]) +
               Dss[i][3] * sum(v == 3 for v in ngram_count[i]) +
               Dss[i][4] * sum(v >= 4 for v in ngram_count[i])) / totals[i]
              for i in range(N)]

    # EM
    E = 1.0e-10
    ps = [1.0 / nalphs, 0]
    for _ in range(1000):
        ngammas = [0.0 for i in range(N)]
        for a in allalphs:
            ps[1] = (ngram_count[0][a] - Dss[0][D_index(0, a)]) / totals[0] + gammas[0] * ps[0]
            s = sum(gammas[i] * ps[i] for i in range(N))
            for i in range(N):
                ngammas[i] += gammas[i] * ps[i] / s
        for i in range(N):
            ngammas[i] /= float(nalphs)

        # print _, ", ".join(str(g) for g in ngammas)
        if all(abs(gammas[i] - ngammas[i]) < E for i in range(N)):
            break
        gammas = ngammas

    alph_probs = [(ngram_count[1][a] - Dss[1][D_index(1, a)]) / totals[1] + gammas[1] *
                  ((ngram_count[0][a] - Dss[0][D_index(0, a)]) / totals[0] + gammas[0] / float(nalphs))
                  for a in allalphs]

    d = 0.10001
    discount = sum(p * d for p in alph_probs)
    alph_probs[1:] = [p * (1.0 - d) for p in alph_probs[1:]]
    alph_probs[0] += discount

    prob_total = sum(alph_probs)
    alph_probs = [p / prob_total for p in alph_probs]

    with open("models/{0}.model".format(chr(given + ord('a'))), "w") as model:
        model.write("\n".join("{0:20.17e}".format(p) for p in alph_probs))


if __name__ == "__main__":
    for i in range(26):
        try:
            gen_model(i)
            print(chr(i + ord('a')))
        except ZeroDivisionError:
            pass
