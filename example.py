#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
import operator
import pyquery
import jpname


def print_topk(papers, k=10):
    for i, (title, authors) in enumerate(papers):
        prob = jpname.names_prob(authors)
        papers[i] = (prob, title, authors)

    papers.sort(reverse=True)
    for i in range(k):
        prob, title, authors = papers[i]
        print(f'Title: {title}')
        print(f'Authors: {prob:.5}')
        longest = len(max(authors, key=len))
        form = f'* {{:{longest}}}  {{:.5}}'
        for author in authors:
            p = jpname.jpname_prob(author)
            print(form.format(author, p))
        print()


def sigmod2018(k=10):
    url = 'https://sigmod2018.org/sigmod_research_list.shtml'
    with urllib.request.urlopen(url) as f:
        txt = f.read()
    pq = pyquery.PyQuery(txt)
    paper_list = pq('#maincontent')[0].getchildren()[1].getchildren()[0].getchildren()
    papers = []
    for paper in paper_list:
        title = paper.getchildren()[0].text.strip()
        authors = paper.text_content().split(title)[1]
        authors = [author.split('(')[0].strip().replace('  ', ' ')
                   for author in authors.split(';')]
        papers.append((title, authors))

    print_topk(papers, k)


if __name__ == '__main__':
    sigmod2018()
