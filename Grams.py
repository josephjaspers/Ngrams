import csv
import sys
import copy
import operator
import random
csv.field_size_limit(sys.maxsize)


class NGram:

    __lst_wordCorpus = ""             # The entire word corpus
    __lst_wordCorpusSet = []          # The set of the word corpus
    __int_corpusLength = 0
    __int_corpusLengthSet = 0
    __lstmap_gramProbabilities = []  # array of maps of gram probabilities ie lst_gramProbabilities[0] returns unigram prob
    __lstmap_gramCounts = []         # same as above but with counts
    __lstlst_orderedProbLst = []
    __lstlst_orderedCountLst = []

    def __init__(self, lst_word_corpus=[""]):
        self.__lst_wordCorpus = lst_word_corpus
        self.__lst_wordCorpusSet = set(lst_word_corpus)
        self.__int_corpusLength = len(lst_word_corpus)
        self.__int_corpusLengthSet = len(self.__lst_wordCorpusSet)

    # ----------------------------Simple Accessors------------------------------------------------#
    # returns a list of maps
    def get_gram_probabilities(self):
        return self.__lstmap_gramProbabilities

    # returns a list of maps
    def get_gram_counts(self):
        return self.__lstmap_gramCounts

    def get_corpus_length(self):
        return self.__int_corpusLength

    def get_corpus_set_length(self):
        return self.__int_corpusLengthSet

    # These are index base 1 for consistency with length of n-gram
    # Returns the Ngram (probability or count) of the given integer
    def get_gram_probability(self, int_gram_index):
        if len(self.__lstmap_gramProbabilities) < int_gram_index:
            self.calculate(int_gram_index)
        return self.__lstmap_gramProbabilities[int_gram_index - 1]

    def get_gram_count(self, int_gram_index):
        if len(self.__lstmap_gramCounts) < int_gram_index:
            self.calculate(int_gram_index)
        return self.__lstmap_gramCounts[int_gram_index - 1]

    # returns a sorted list of pairs from the corresponding probability map
    def get_gram_probability_ordered(self, int_gram_index):
        if len(self.__lstmap_gramProbabilities) < int_gram_index:
            self.calculate(int_gram_index)

        return self.__lstlst_orderedProbLstLst[int_gram_index - 1]

    # returns a sorted list of pairs from the corresponding probability map
    def get_gram_count_ordered(self, int_gram_index):
        if len(self.__lstmap_gramCounts) < int_gram_index:
            self.calculate(int_gram_index)

        return self.__lstlst_orderedCountLst[int_gram_index - 1]


    # ----------------------------Simple Mutators------------------------------------------------#
    def set_text(self, lst_word_corpus):
        self.__lst_wordCorpus = lst_word_corpus
        self.__lst_wordCorpusSet = set(lst_word_corpus)
        self.__int_corpusLength = len(lst_word_corpus)
        self.__int_corpusLengthSet = len(self.__lst_wordCorpusSet)

    # ---------------------------Private helper method for n gram count--------------------------#
    def __ngram_count(self, int_ngram_length):
        # number of grams in a given text in respect to gram_order
        def numb_grams():
            return self.__int_corpusLength - int_ngram_length

        # get the specific gram at a given text and gram length
        def gram_at(index, gram_index=int_ngram_length): # gram index can also be interperted as gram_length
            if gram_index > 1:
                return gram_at(index, gram_index - 1) + " " + self.__lst_wordCorpus[index + gram_index]
            else:
                return self.__lst_wordCorpus[index]

        # ---- Actual Function Implementation ---- #
        map_word_count = {}

        # count the number of times a gram occurs
        for i in range(0, numb_grams()):
            if gram_at(i) in map_word_count:
                map_word_count[gram_at(i)] += 1
            else:
                map_word_count[gram_at(i)] = 1

        self.__lstmap_gramCounts.append(map_word_count)

    # ---- function to calculate the probabilities of all grams of given length in a text ---- #
    # ---- Also calculates all counts and probabilities of the n-grams of length less than the given Length ----#
    # ---- DO NOT GIVE A USER VALUE FOR INT_MIN_COUNT
    def calculate(self, int_ngram_length, int_min_count=0):
        # clear everything
        self.__lstmap_gramCounts = []
        self.__lstmap_gramProbabilities = []
        self.__lstlst_orderedCountLst = []
        self.__lstlst_orderedProbLst = []

        # calculate the count of each gram (IE 3 calculates unigram bigram and trigram)
        for i in range(1, int_ngram_length + 1):
            self.__ngram_count(i)

        if int_min_count > 0:
            lstmap_thresholded = []
            for _map in self.__lstmap_gramCounts:
                lstmap_thresholded.append({k : v for k,v in _map.items() if v >= int_min_count})
            self.__lstmap_gramCounts = lstmap_thresholded
            print(self.__lstmap_gramCounts)

        for lstmap in self.__lstmap_gramCounts:
            for k, v in lstmap.items():
                if lstmap[k] < int_min_count:
                    del lstmap[k]

        # copy to probabilities
        self.__lstmap_gramProbabilities = copy.deepcopy(self.__lstmap_gramCounts)

        # calculate the probabilities of a unigram
        for k, v in self.__lstmap_gramProbabilities[0].items():
            self.__lstmap_gramProbabilities[0][k] = v / self.__int_corpusLength           # divide by corpus length to get unigram prob

        # calculate the remaining probabilities of the ngrams
        for i in range(1, len(self.__lstmap_gramProbabilities)):
            for k, count in self.__lstmap_gramProbabilities[i].items():
                self.__lstmap_gramProbabilities[i][k] = count / self.__lstmap_gramCounts[i - 1][" ".join(k.split(' ')[0:i])]

        # for each gram -sort the count and  probability lists and store
        for n_gram in self.__lstmap_gramProbabilities:
            self.__lstlst_orderedProbLst.append(sorted(n_gram.items(), key=operator.itemgetter(1)))

        for n_gram in self.__lstmap_gramCounts:
            self.__lstlst_orderedCountLst.append(sorted(n_gram.items(), key=operator.itemgetter(1)))

        return self.__lstmap_gramProbabilities

    def random_sentence_base(self, int_gram):
        # returns a random subphrase in the corpus

        if int_gram > len(self.__lstmap_gramCounts):
            self.calculate(int_gram)

        sz = len(self.__lstmap_gramCounts[int_gram - 1])
        base = self.__lstlst_orderedCountLst[int_gram - 1][random.randint(0, sz)][0]
        return ' '.join(base.split(' ')[0:-1])  # get a base phrase the size of the gram - 1

    def random_sentence_next(self, curr_sentence, int_gram):

        def pair_list_sum(pair_lst):
            return sum([pair[1] for pair in pair_lst])

        def last(str_):
            return str_.split(' ')[-1]

        def get_random_word(pair_lst):
            random_position = random.random() * pair_list_sum(pair_lst)
            flt_pos = 0

            for i in range(0, len(pair_lst)):
                if i + 1 == len(pair_lst):
                    return pair_lst[i][0]

                if (flt_pos >= random_position) and (flt_pos <= random_position + pair_lst[i + 1][1]):
                    return pair_lst[i][0]
                flt_pos += pair_lst[i][1]

            return ' '

        relevant_sent = ' '.join(curr_sentence.split(' ')[-int_gram:])
        possible_words = [(last(k), v) for k, v in self.__lstlst_orderedCountLst[int_gram - 1] if k[0:len(relevant_sent)] == relevant_sent]

        return get_random_word(possible_words)

