Last Updated: March 20, 2018
Author: JosephJaspers

NGrams is a simple script used to calculate nGrams from a given text corpus (a list of strings).
The NGrams itself does not do any text processing on the data itself and simply calculates the ngrams.
The Recursive implementation enables the short script to scale to any order of NGrams. 

The class stores the following data which is accessible through simple get methods:
	
    __lst_wordCorpus = ""             	# The entire word corpus
    __lst_wordCorpusSet = []          	# The set of the word corpus
    __int_corpusLength = 0			# length of the entire corpus
    __int_corpusLengthSet = 0		# length of the set of the corpus (unique words)
    __lstmap_gramProbabilities = []   	# list of maps corresponding to every gram in the corpus and their probabilities 
    __lstmap_gramCounts = []          	# list of maps corresponding to every gram in the corpus and their probabilities 
    __lstlst_orderedProbLst = []      	# list of pairs (ordered greatest to least by probability) of same word,probability relationship
    __lstlst_orderedCountLst = []     	# list of pairs (ordered greatest to least by count) of same word,count relationship

The method list is as follows:

	return type			function name			parameters
	list<map<string, float>> 	get_gram_probabilities		(void)
	int 				get_corpus_length		(void)
	int 				get_corpus_set_length		(void)
	map<string, float> 		get_gram_probability		(int_gram_order)
	map<string, inr> 		get_gram_count			(int_gram_order)
	list<pair<string, float>> 	get_gram_probability_ordered	(int_gram_order)
	list<pair<string, int>> 	get_gram_count_ordered		(int_gram_order)
	list<map<string, float>> 	calculate			(int_gram_order, int_threshold)
	string 				random_sentence_base		(int_gram)
	string 				random_sentence_next		(curr_sentence, int_gram)

	function name			Elaboration 
	get_gram_probabilities		Returns the list of all maps of string, floats. 
	get_gram_counts			Returns the list of all maps of string, int. 
	get_corpus_length		Returns length of corpus
	get_corpus_set_length		Returns the number of unique words
	get_gram_probability		Returns a map of <Word, Probabilities> of the given Ngram
	get_gram_count			Returns a map of <Word, Counts> of the given Ngram
	get_gram_probability_ordered	Returns a sorted list of pairs <Word,Probabilities> of the given Ngram
	get_gram_count_ordered		Returns a sorted list of pairs <Word,Counts> of the given Ngram
	calculate			Calculates all Ngrams from order 0 to the given param
	random_sentence_base		Returns a valid base_phrase of the given Ngram
	random_sentence_next		Returns a possible word based upon the given sentence and Ngram



