import nltk
import re
import string
import random
import csv
import sys
import copy
import operator
import datetime
from Grams import *


# convert all columns in a given list from all files given into a single value
def file_to_string(column_lst, *filenames):
    str_combined = ""
    for fname in filenames:
        with open(fname) as csvfile:
            article = csv.reader(csvfile)
            for row in article:
                str_combined += '\n'
                for i in column_lst:
                    str_combined += row[i]
    return str_combined


# removes punctuation and lowercases
def normalize(str_data):
    str_data = str_data.lower()
    return str_data


# returns a list from a list of pairs with the value being at least min
def minimum_rep_lst(lst_pair_wordprob, min_reps):
    return [pair for pair in lst_pair_wordprob if pair[1] >= min_reps]


def random_sentence(gram, order=1, sentence_length=10):
    sentence = gram.random_sentence_base(order) + ' '

    concat = ""
    for i in range(0, sentence_length):
        concat = gram.random_sentence_next(sentence, order) + " "
        sentence += concat

    return sentence


def print_core_data(ngram):
    print("CorpusLength: ", ngram.get_corpus_length())
    print("Total vocab: ", ngram.get_corpus_set_length())


def print_data(ngram, int_gram_order):
    sentence_length = 10

    orderedP = ngram.get_gram_probability_ordered(int_gram_order)
    orderedC = ngram.get_gram_count_ordered(int_gram_order)
    print("\n------------Probability and Count of Gram (top 20)", int_gram_order, "------------")
    print(orderedP[0:15])
    print(orderedC[0:15])
    print("\n-------------Generated Sentences (max length=", sentence_length, ")")
    print("SENTENCE1 ", random_sentence(ngram, int_gram_order, sentence_length))
    print("SENTENCE2 ", random_sentence(ngram, int_gram_order, sentence_length))
    print("SENTENCE3 ", random_sentence(ngram, int_gram_order, sentence_length))


def run_project(str_filename, lst_columns, mincount=0):
    str_data = file_to_string(str_filename, lst_columns)
    print("Parsing...")
    news_text = normalize(str_data)
    tokenized = nltk.word_tokenize(news_text)

    print("\n")
    print("------------------------Calculating nGrams------------------------")
    gram = NGram(tokenized)
    print_core_data(gram)
    gram.calculate(3, mincount)     # calculate the ngrams for unigram,bigram,trigram (1-3) with a minimum repeats
    print_data(gram, 3)
    print_data(gram, 2)
    print_data(gram, 1)

    return gram


NEWS_COL_INDEX = [9]
WINE_COL_INDEX = [1]

# run_project (param1 = a list of columns to read, param2= filepath for the CSV)
newsGram1 = run_project(NEWS_COL_INDEX, "/home/joseph/Documents/NLP_Grams/all-the-news/articles1.csv", 20)
del newsGram1
newsGram2 = run_project(NEWS_COL_INDEX, "/home/joseph/Documents/NLP_Grams/all-the-news/articles2.csv", 20)
del newsGram2
newsGram3 = run_project(NEWS_COL_INDEX, "/home/joseph/Documents/NLP_Grams/all-the-news/articles3.csv", 20)
del newsGram3
wineGram1 = run_project(NEWS_COL_INDEX, "/home/joseph/Documents/NLP_Grams/wine-reviews/winemag-data-130k-v2.csv", 20)
del wineGram1
wineGram2 = run_project(NEWS_COL_INDEX, "/home/joseph/Documents/NLP_Grams/wine-reviews/winemag-data_first150k.csv", 20)
del wineGram2

