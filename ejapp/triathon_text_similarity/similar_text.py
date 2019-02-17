import pandas as pd
import numpy as np
from string import punctuation
from collections import Counter
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from difflib import SequenceMatcher

class similar_text_score:
    def similarity_score(self, txt_true, txt_pred, sample_weight = None):

        # converting both type of texts to lowercase
        txt_true = txt_true.lower()
        txt_pred = txt_pred.lower()
        
        #removing all the punctuation marks from the texts
        processed_txt_true =''.join([word for word in txt_true if word not in punctuation])
        processed_txt_pred =''.join([word for word in txt_pred if word not in punctuation])
        
        #creating a list containing invidual statements in eachline
        processed_txt_true_split = processed_txt_true.splitlines()
        processed_txt_pred_split = processed_txt_pred.splitlines()

        # creating a bag of words
        all_txt_true = ' '.join(processed_txt_true_split)
        all_txt_pred = ' '.join(processed_txt_pred_split)
        
        # creating lists containing each words from individual input texts
        all_txt_true_words_list = all_txt_true.split()
        all_txt_pred_words_list = all_txt_pred.split()

        #Counter is used to how many times a word occured
        counts_txt_true = Counter(all_txt_true_words_list)
        counts_txt_pred = Counter(all_txt_pred_words_list)

        # sorts the words in decreasing order of occurance
        vocab_txt_true = sorted(counts_txt_true, key = counts_txt_true.get, reverse = True)
        vocab_txt_pred = sorted(counts_txt_pred, key = counts_txt_pred.get, reverse = True)
        
        # use stopwords to remove irrelevant words
        ps = PorterStemmer()
        vocab_txt_true = [ps.stem(word) for word in vocab_txt_true if not word in set(stopwords.words('english'))]
        vocab_txt_pred = [ps.stem(word) for word in vocab_txt_pred if not word in set(stopwords.words('english'))]

        # convert lists of words to string files
        vocab_txt_true = ' '.join(vocab_txt_true)
        vocab_txt_pred = ' '.join(vocab_txt_pred)

        return SequenceMatcher(None,vocab_txt_true,vocab_txt_pred).ratio()