import csv
import nltk
import sys
import copy
import operator
csv.field_size_limit(sys.maxsize)


class NGram:

    lst_wordCorpus = ""             # The entire word corpus
    lst_wordCorpusSet = []          # The set of the word corpus
    int_corpusLength = 0
    int_corpusSetLength = 0
    lst_gramProbabilities = []  # array of maps of gram probabilities ie lst_gramProbabilities[0] returns unigram prob
    lst_gramCounts = []         # same as above but with counts

    def __init__(self, lst_word_corpus=[""]):
        self.lst_wordCorpus = lst_word_corpus
        self.lst_wordCorpusSet = set(lst_word_corpus)
        self.int_corpusLength = len(lst_word_corpus)
        self.int_corpusLengthSet = len(self.lst_wordCorpusSet)

    # ----------------------------Simple Accessors------------------------------------------------#
    # returns a list of maps
    def get_probabilities(self):
        return self.lst_gramProbabilities

    # returns a list of maps
    def get_counts(self):
        return self.lst_gramCounts

    # These are index base 1 for consistency with length of n-gram
    # Returns the Ngram (probability or count) of the given integer
    def get_probability_gram(self, int_gram_index):
        if len(self.lst_gramProbabilities) < int_gram_index:
            self.calculate(int_gram_index)
        return self.lst_gramProbabilities[int_gram_index - 1]

    def get_count_gram(self, int_gram_index):
        if len(self.lst_gramCounts) < int_gram_index:
            self.calculate(int_gram_index)
        return self.lst_gramCounts[int_gram_index - 1]

    # returns a sorted list of pairs from the corresponding probability map
    def get_probability_gram_ordered(self, int_gram_index):
        if len(self.lst_gramProbabilities) < int_gram_index:
            self.calculate(int_gram_index)

        lst_srt_gram_sorted = sorted(self.lst_gramProbabilities[int_gram_index - 1].items(), key=operator.itemgetter(1))
        lst_srt_gram_sorted.reverse()
        return lst_srt_gram_sorted

    # returns a sorted list of pairs from the corresponding probability map
    def get_count_gram_ordered(self, int_gram_index):
        if len(self.lst_gramCounts) < int_gram_index:
            self.calculate(int_gram_index)

        lst_srt_gram_sorted = sorted(self.lst_gramCounts[int_gram_index - 1].items(), key=operator.itemgetter(1))
        lst_srt_gram_sorted.reverse()
        return lst_srt_gram_sorted

    # ----------------------------Simple Mutators------------------------------------------------#
    def set_text(self, lst_word_corpus):
        self.lst_wordCorpus = lst_word_corpus
        self.lst_wordCorpusSet = set(lst_word_corpus)
        self.int_corpusLength = len(lst_word_corpus)
        self.int_corpusLengthSet = len(self.lst_wordCorpusSet)

    # ---------------------------Private helper method for n gram count--------------------------#
    def __ngram_count(self, int_ngram_length):
        # number of grams in a given text in respect to gram_order
        def numb_grams():
            return self.int_corpusLength - int_ngram_length

        # get the specific gram at a given text and gram length
        def gram_at(index, gram_index=int_ngram_length): # gram index can also be interperted as gram_length
            if gram_index > 1:
                return gram_at(index, gram_index - 1) + " " + self.lst_wordCorpus[index + gram_index]
            else:
                return self.lst_wordCorpus[index]

        # ---- Actual Function Implementation ---- #
        map_word_count = {}

        # count the number of times a gram occurs
        for i in range(0, numb_grams()):
            if gram_at(i) in map_word_count:
                map_word_count[gram_at(i)] += 1
            else:
                map_word_count[gram_at(i)] = 1

        return map_word_count

    # ---- function to calculate the probabilities of all grams of given length in a text ---- #
    # ---- Also calculates all counts and probabilities of the n-grams of length less than the given Length ----#
    def calculate(self, int_ngram_length):
        ngram_counts = []

        for i in range(1, int_ngram_length + 1):
            ngram_counts.append(self.__ngram_count(i))

        ngram_probs = copy.deepcopy(ngram_counts)

        # calculate the probabilities of a unigram
        for k, v in ngram_probs[0].items():
            ngram_probs[0][k] = v / self.int_corpusLength           # divide by corpus length to get unigram prob

        # calculate the remaining probabilities of the ngrams
        for i in range(1, len(ngram_probs)):
            int_total_grams = self.int_corpusLength - int_ngram_length
            for k, count in ngram_probs[i].items():
                # first we divide by the total number of n grams, and then by the probability of the n_gram below it
                # P(W_n-1 | W_n) = count / int_total_grams
                # P(W_n-1) =  ngram_probs[i - 1][" ".join(k.split(' ')[0:i])]
                # ergo....   P(W_n-1 | W_n) / P(W_n-1) == count / ngram_probs[i - 1][" ".join(k.split(' ')[0:i])] / int_total_grams
                ngram_probs[i][k] = count / ngram_probs[i - 1][" ".join(k.split(' ')[0:i])] / int_total_grams

        self.lst_gramProbabilities = ngram_probs
        self.lst_gramCounts = ngram_counts
        return ngram_probs


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
    # There are like 7 versions of apostrophes in python
    punctuation = [',', '.', '.', '"', "'", '/', '?', '!', '/', ':', "'", '’', '‘', '- ', ' -', ' - ', '-', ' -', ' -']
    str_data = "".join([char for char in str_data if char not in punctuation])
    str_data = str_data.lower()

    return str_data


TEXT_COL_INDEX = 2
print("reading f1 (news)")
str_news = file_to_string([TEXT_COL_INDEX], "/home/joseph/Documents/NLP_Grams/all-the-news/articles1.csv")
print("reading f2 (news)")
str_news += file_to_string([TEXT_COL_INDEX], "/home/joseph/Documents/NLP_Grams/all-the-news/articles2.csv")
print("reading f3 (news)")
str_news += file_to_string([TEXT_COL_INDEX], "/home/joseph/Documents/NLP_Grams/all-the-news/articles3.csv")
print("reading f4 (wine)")
str_wine = file_to_string([TEXT_COL_INDEX], "/home/joseph/Documents/NLP_Grams/wine-reviews/winemag-data-130k-v2.csv")
print("reading f5 (wine)")
str_wine += file_to_string([TEXT_COL_INDEX], "/home/joseph/Documents/NLP_Grams/wine-reviews/winemag-data_first150k.csv")


print("normalizing the data ")
news_text = normalize(str_news)
wine_text = normalize(str_wine)
print("Tokenized the string")
news_tokenized = nltk.word_tokenize(news_text)
wine_tokenized = nltk.word_tokenize(wine_text)

print("\n")
print("------------------------Calculating for news_text------------------------")
myGram = NGram(news_tokenized)
myGram.calculate(3)     # calculate the ngram count and probabilities from length 1 to 3 (inclusive)
                        # use calculate first as it caches all the values from unigram-to the given n gram]

print("\n------------Probability and Count of news (trigram)------------")
print(myGram.get_probability_gram_ordered(3)[0:10])
print(myGram.get_count_gram_ordered(3)[0:10])
print("\n------------Probability and Count of news (bigram)------------")
print(myGram.get_probability_gram_ordered(2)[0:10])
print(myGram.get_count_gram_ordered(2)[0:10])
print("\n------------Probability and Count of news (unigram)------------")
print(myGram.get_probability_gram_ordered(1)[0:10])
print(myGram.get_count_gram_ordered(1)[0:10])

print("\n \n------------------------Recalculating for wine_text------------------------")
myGram.set_text(wine_text)
myGram.calculate(3)

print("\n------------Probability and Count of wine (trigram)------------")
print(myGram.get_probability_gram_ordered(3)[0:10])
print(myGram.get_count_gram_ordered(3)[0:10])
print("\n------------Probability and Count of wine (bigram)------------")
print(myGram.get_probability_gram_ordered(2)[0:10])
print(myGram.get_count_gram_ordered(2)[0:10])
print("\n------------Probability and Count of wine (unigram)------------")
print(myGram.get_probability_gram_ordered(1)[0:10])
print(myGram.get_count_gram_ordered(1)[0:10])




