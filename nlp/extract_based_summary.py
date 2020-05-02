# extract-based: document -> sentence similarity -> weight sentences -> select sentences with higher rank
# https://blog.floydhub.com/gentle-introduction-to-text-summarization-in-machine-learning/
# abstract-based: document -> understand context -> semantics -> create own summary
# https://www.analyticsvidhya.com/blog/2019/06/comprehensive-guide-text-summarization-using-deep-learning-python/

import bs4 as BeautifulSoup
import urllib.request
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
# from nltk import word_tokenize
from nltk.tokenize import word_tokenize, sent_tokenize

# set up
# nltk.download('punkt')
# nltk.download('stopwords')

# Fetching the content from the URL
fetched_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/20th_century')
article_read = fetched_data.read()
# Parsing the URL content and storing in a variable
article_parsed = BeautifulSoup.BeautifulSoup(article_read,'html.parser')
# Returning <p> tags
paragraphs = article_parsed.find_all('p')

article_content = '''Introduction to Mina Mina Myoui (2# Myõi Mina), known mostly as Mina (Hangul: 014), was born on March 24, 1997 in San Antonio, Texas, and moved to Kobe, Japan, when she was a toddler. She is a vocalist and lead dancer of the group. In 2013, she was scouted by a JYP Entertainment staff member while shopping with her mother and was invited to join JYP Entertainment Global. She auditioned in a JYP audition in Japan and joined the trainee program in South Korea on January 2, 2014. Age 23 Debut Oct 20, 2015 '''
# Looping through the paragraphs and adding them to the variable
# for p in paragraphs:  
#     article_content += p.text
# # testing
# article_content = "Mina Myoui (2# Myõi Mina), known mostly as Mina (Hangul: 014), was born on March 24, 1997 in San Antonio, Texas, and moved to Kobe, Japan, when she was a toddler. She is a vocalist and lead dancer of the group. In 2013, she was scouted by a JYP Entertainment staff member while shopping with her mother and was invited to join JYP Entertainment Global. She auditioned in a JYP audition in Japan and joined the trainee program in South Korea on January 2, 2014."

# Processing the data
# print(article_content)
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
sentences = sent_tokenize(article_content)
frequency_table = _create_dictionary_table(article_content)

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

sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

print("\nsentences: \n", sentences)
print("\nfrequency_table: \n", frequency_table)
print("\nsentence_scores: \n", sentence_scores)

# Threshold of the sentences
def _calculate_average_score(sentence_weight) -> int:
    # Calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]
    # Getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))
    return average_score
    

threshold = _calculate_average_score(sentence_scores)

print("\nthreshold: \n", threshold)

# Getting the summary
def _get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''
    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1
    return article_summary

def server_get_summary(article_content, threshold):
    sentences = sent_tokenize(article_content)
    frequency_table = _create_dictionary_table(article_content)
    sentence_weight = _calculate_sentence_scores(sentences, frequency_table)

    sentence_counter = 0
    article_summary = ''
    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1
    return article_summary

# k * threshold, threshold increases -> summary size decreases
article_summary = _get_article_summary(sentences, sentence_scores, 1.1 * threshold)

print("raw text \n")
print(article_content)
print("summary \n")
print(article_summary)
