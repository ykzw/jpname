#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
import urllib.request
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


def kdd2018(k=10):
    url = 'http://www.kdd.org/kdd2018/accepted-papers'
    with urllib.request.urlopen(url) as f:
        txt = f.read()
    pq = pyquery.PyQuery(txt)
    paper_list = pq('.media-body')
    papers = []
    for paper in paper_list:
        title = paper.getchildren()[0].text.split(':')[1].strip()
        authors = paper.getchildren()[1].text_content().strip()
        authors = [author.split('(')[0].strip()
                   for author in authors.split(';')]
        papers.append((title, authors))

    print_topk(papers, k)


if __name__ == '__main__':
    # sigmod2018()
    kdd2018()
