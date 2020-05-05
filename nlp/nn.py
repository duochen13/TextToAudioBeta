import pandas as pd
import tensorflow as tf
import nltk
from matplotlib import pyplot as plt
from nltk import sent_tokenize


content = '''Introduction to Mina Mina Myoui (2# Myõi Mina), known mostly as Mina (Hangul: 014), was born on March 24, 1997 in San Antonio, Texas, and moved to Kobe, Japan, when she was a toddler. She is a vocalist and lead dancer of the group. In 2013, she was scouted by a JYP Entertainment staff member while shopping with her mother and was invited to join JYP Entertainment Global. She auditioned in a JYP audition in Japan and joined the trainee program in South Korea on January 2, 2014. Age 23 Debut Oct 20, 2015 '''

# nltk.download('punkt')
sentences = sent_tokenize(content, language='en')

print(sentences)
