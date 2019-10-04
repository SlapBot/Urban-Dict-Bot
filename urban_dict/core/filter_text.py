import operator
from nltk import word_tokenize
from nltk.corpus import stopwords
from urban_dict.core.word_frequency_list import word_frequency


class FilterText(object):
    def __init__(self):
        self.words = []

    def filter(self, text):
        self.words = self.clean_words(text)
        if len(self.words) == 0:
            return False
        known_results, unknown_results = self.search()
        return known_results, unknown_results

    def search(self):
        known_results = []
        unknown_results = []
        for word in self.words:
            result = self.find_rank_and_frequency(word)
            if result:
                known_results.append(result)    # word, rank and frequency as array
            else:
                unknown_results.append([word, len(word), None])   # word, length of word and None as array
        known_results.sort(key=operator.itemgetter(1), reverse=True)
        unknown_results.sort(key=operator.itemgetter(1), reverse=True)
        print("Known results: %s, Unknown results: %s" % (known_results, unknown_results))
        return known_results, unknown_results

    @staticmethod
    def clean_words(text):
        words_list = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        non_duplicate_words = list(set(words_list))
        filtered_sentence_array = [w for w in non_duplicate_words if not w in stop_words]
        valid_words = []
        for word in filtered_sentence_array:
            if word.isalnum():
                valid_words.append(word)
        return valid_words

    @staticmethod
    def find_rank_and_frequency(word):
        for defined_word in word_frequency:
            if word.lower() == defined_word[1].lower():
                return [word, int(defined_word[0]), int(defined_word[3])]
        return False
