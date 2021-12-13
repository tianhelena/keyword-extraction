#!/usr/bin/env python

import sys
import operator
from rake_nltk import Rake
from os import listdir
from os.path import isfile, join
from collections import Counter
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from more_itertools import take

def get_text(filename):
    with open(filename) as f:
        data = f.read()
    return data

def run_analysis(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases_with_scores()


def get_files(dir):
    return [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]

def valid_term(term):
    blocklist_words = [
        'content',
        'footer',
        'blog',
        'filter',
        'via',
        'wrapper',
        'instagram',
        'twitter',
        'facebook',
        'copyright',
        "addthis",
        "advanced settings",
        "december",
        "40",
        "related posts metals demand",
        "podcasts",
        "percentage",
    ]
    return not any([blocked in term for blocked in blocklist_words])


def word_frequency_horizontal_bar_chart(counter):
    top_n = 20
    words = [term for (term, files) in take(top_n ,counter.items())]
    counts = [len(files) for (term, files) in take(top_n, counter.items())]

    plt.rcdefaults()
    fig, ax = plt.subplots()
    y_pos = np.arange(top_n)

    ax.barh(y_pos, counts, align='center')
    ax.set_yticks(y_pos, labels=words)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Word Counts')
    ax.set_title('Keyword Counts From All 2021 IMF Blogs')

    plt.show()

def print_counter(counter):
    for term, mentions in counter.items():
        print('\n')
        print(f'{term} : {mentions}')

if __name__ == '__main__':
    files = get_files(sys.argv[1])
    keywords = [(file, term) for file in files for (score, term) in run_analysis(get_text(file)) if score > 6.0 and valid_term(term)]
    counter = defaultdict(set)

    for (file, term) in keywords:
        counter[term].add(file)

    counter = (dict(sorted(counter.items(), key=lambda x: len(x[1]), reverse=True)))
    word_frequency_horizontal_bar_chart(counter)


# python3 test.py ./articles/inflation.txt
