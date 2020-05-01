import bs4 as BeautifulSoup
import urllib.request
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
# from nltk import word_tokenize
from nltk.tokenize import word_tokenize, sent_tokenize


# article_content = '''Most living animal species are in the Bilateria, a clade whose members have a bilaterally symmetric body plan. The Bilateria include the protostomes—in which many groups of invertebrates are found, such as nematodes, arthropods, and molluscs—and the deuterostomes, containing both the echinoderms as well as the chordates, the latter containing the vertebrates. Life forms interpreted as early animals were present in the Ediacaran biota of the late Precambrian. Many modern animal phyla became clearly established in the fossil record as marine species during the Cambrian explosion, which began around 542 million years ago. 6,331 groups of genes common to all living animals have been identified; these may have arisen from a single common ancestor that lived 650 million years ago.'''

# Processing the data
def _create_dictionary_table(text_string) -> dict:
    # Removing stop words
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    # Reducing words to their root form
    stem = PorterStemmer()
    # Creating dictionary for the word frequency table
    frequency_table = dict()
    for wd in words:
        wd = stem.stem(wd)
        if wd in stop_words:
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1
    return frequency_table

# Tokenizing the article into sentences
# sentences = sent_tokenize(article_content)
# frequency_table = _create_dictionary_table(article_content)

# Calculate weighted frequencies of the sentences
def _calculate_sentence_scores(sentences, frequency_table) -> dict:   
    # Algorithm for scoring a sentence by its words
    sentence_weight = dict()
    for sentence in sentences:
        sentence_wordcount = (len(word_tokenize(sentence)))
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] = frequency_table[word_weight]
        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] /        sentence_wordcount_without_stop_words
    return sentence_weight

# sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

# Threshold of the sentences
def _calculate_average_score(sentence_weight) -> int:
    # Calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]
    # Getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))
    return average_score
    
# threshold = _calculate_average_score(sentence_scores)

# Getting the summary
def _get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''
    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1
    return article_summary
