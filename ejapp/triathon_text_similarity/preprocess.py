import numpy as np
import pandas as pd
from string import punctuation

with open("/media/mrugank/626CB0316CB00239/for development purpose only/python/triathon_text_similarity/data.txt","r") as f :
    review = f.read()

dataset = pd.read_csv('./advocates.tsv', delimiter = '\t', quoting = 3)

counter = 0
input_list = []
compare_list = []
counter = 0

for i in range(1000):
    if dataset['Liked'][i] == 1:
        counter += 1
        if counter < 41:
            input_list.append(dataset['Review'][i])
            #print(input_text)

final_text_str = ''.join(input_list)

for i in range(1000):
    if dataset['Liked'][i] == 1:
        counter += 1
        if counter > 41:
            compare_list.append(dataset['Review'][i])
            #print(input_text)

final_compare_text_str = ''.join(compare_list)

len(final_compare_text_str)
len(final_text_str)

compare_text = final_compare_text_str[:2030]
len(compare_text)

print(punctuation)
review
review = review.lower()

final_text_str = final_text_str.lower()
compare_text = compare_text.lower()

all_text = ''.join([c for c in final_text_str if c not in punctuation])
all_text
all_comp_text = ''.join([c for c in compare_text if c not in punctuation])
all_comp_text
all_text.find('wow')

reviews_split = all_text.splitlines()
reviews_split

reviews_comp_split = all_comp_text.splitlines()
reviews_comp_split

'''all_text = ' '.join(reviews_split)
all_text'''

word = all_text.split()
word

comp_word = all_comp_text.split()
comp_word

from collections import Counter
counts = Counter(word)
counts
comp_counts = Counter(comp_word)
comp_counts
'''>>> counts
Counter({'the': 5, 'selection': 1, 'on': 1, 'menu': 1, 'was': 1, 'great': 1, 'and': 1, 'so': 1, 'were': 1, 'prices': 1, 'i': 1, 'tried': 1, 'cape': 1, 'cod': 1, 'ravoli': 1, 'chicken': 1, 'with': 1, 'cranberrymmmm': 1, 'food': 1, 'amazing': 1})'''

vocab = sorted(counts, key = counts.get, reverse = True)
vocab

comp_vocab = sorted(comp_counts, key = comp_counts.get, reverse = True)
comp_vocab

vocab_to_number = {word:ii for ii,word in enumerate(vocab,1)}
vocab_to_number['wow']

vocab_comp_to_number = {word:ii for ii,word in enumerate(comp_vocab,1)}
vocab_comp_to_number['wow']

'''{1: 'the', 2: 'selection', 3: 'on', 4: 'menu', 5: 'was', 6: 'great', 7: 'and', 8: 'so', 9: 'were', 10: 'prices', 11: 'i', 12: 'tried', 13: 'cape', 14: 'cod', 15: 'ravoli', 16: 'chicken', 17: 'with', 18: 'cranberrymmmm', 19: 'food', 20: 'amazing'}'''
reviews_int = []
for review in reviews_split:
    reviews_int.append([vocab_to_number[word] for word in all_text.split()])
    #print(review.split())

reviews_comp_int = []
for review in reviews_comp_split:
    reviews_comp_int.append([vocab_comp_to_number[word] for word in all_comp_text.split()])

print(len(vocab_to_number))
print(reviews_int[0])

print(len(reviews_int[0]))
print(len(reviews_comp_int[0]))

reviews_comp_int[0] = reviews_comp_int[0][:330]

from sklearn.metrics import matthews_corrcoef
y_true = reviews_int[0]
y_pred = reviews_comp_int[0]
'''y_true2 = [1,2,3]
y_pred2 = [0,8,3]'''
matthews_corrcoef(y_true, y_pred) 
