from triathon_text_similarity.prediction import *
from triathon_text_similarity.similar_text import *
from similarity.cosine import Cosine
import pandas as pd

cosine = Cosine(2)

dataset_text = pd.read_csv('./advocates.tsv', delimiter = '\t', quoting = 3)

counter = 0
input_list = []
compare_list = []
for i in range(0,1000):
    if dataset_text['Liked'][i] == 1:
        counter += 1
        if counter < 41:
            input_list.append(dataset_text['Review'][i])
            #print(input_text)

final_text_str = ''.join(input_list)
for i in range(1000):
    if dataset_text['Liked'][i] == 1:
        counter += 1
        if counter > 41:
            compare_list.append(dataset_text['Review'][i])
            #print(input_text)

final_compare_text_str = ''.join(compare_list)
print(final_compare_text_str)
print(input_list)
print(counter)

same = similar_text_score()
txt_true = "The term international child abduction is generally synonymous with international parental kidnapping, child snatching, and child stealing.[1] However, the more precise legal usage of international child abduction originates in private international law and refers to the illegal removal of children from their home by an acquaintance or family member to a foreign country. In this context, 'illegal' is normally taken to mean 'in breach of custodial rights' and 'home' is defined as the child's habitual residence"

txt_pred = "What is today called 'parental kidnapping,' 'international child abduction,', 'parental child abduction' and 'parental child trafficking' has existed as long as different legal jurisdictions and international borders have—though often under different names. None of these names achieved the modern day broad acceptance of terms like international child abduction. Lacking a common set of terminology or specifically designed laws to address the, at the time, poorly defined problem, researchers on the history of cross-border child abduction must search for terms like 'custodial interference,' 'contempt of child custody orders,' 'legal kidnapping' or, in cases where children were viewed more as property than as individual subjects of rights, name variations on theft, child-maintenance debt and smuggling, among others."

y_pred2 = "New Delhi: At least 35 people were killed and over 200 injured on Sunday when over dozen coaches of two superfast Express trains got derailed in Uttar Pradesh and Assam, raising concerns once again about the patchy safety record of Indian Railways.Thirty-five have been confirmed dead and over 140 injured as the Howrah-Delhi-Kalka Express got derailed near Fatehpur Malwa in Uttar Pradesh. The incident took place around 12:30 pm. Approximately 1200 people were travelling on board Kalka Mail.The train was travelling from Howrah to New Delhi and was moving at the speed of 108 Km/Hr when the driver used emergency brakes to slow it down, which led to the derailment, sources claimed."

print(lcs.distance(final_text_str, final_compare_text_str))

print(qgram.distance('hello', 'world'))

print(cosine.similarity_profiles(cosine.get_profile(final_text_str), cosine.get_profile(final_compare_text_str)))

print(jarowinkler.similarity(final_text_str, final_compare_text_str))

same.similarity_score(txt_true = final_text_str, txt_pred = final_compare_text_str)

pred = prediction()
pred.generate_a_dataset(qnt_of_rand_num = 200, dataset_name = 'lawers200.csv')
pred.train_model(csv_file = 'lawers200.csv', save_model_name = 'model200.pickle')
pred.load_model_and_pred(model_name = 'model200.pickle',rating = 0.95, wins = 6, time_diff = 196)

import numpy as np 
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle

def find_accuracy(dataset_name = 'lawers200.csv', model_name = 'model200.pickle'):
    y_true = []
    y_pred = []
    ss_res = 0
    ss_total = 0
    sum_y_true = 0
    counter = 0
    dataset = pd.read_csv(dataset_name)
    #print(len(dataset))
    #print(type(dataset['Ratings']))
    for i in dataset['Score']:
        y_true.append(i)
    # loading the saved model
    pickle_in = open(model_name, 'rb')
    regressor = pickle.load(pickle_in)
    for i in range(0,200):
        each_row = dataset.iloc[i,:].values
        pred = regressor.predict([[each_row[0],each_row[1],each_row[2]]])
        #print(pred)
        y_pred.append(pred[0])
    #for i in dataset:
        #print(i)
    #print(y_pred)
    for i in range(0, 200):
        single_mse = (y_true[i] - y_pred[i])**2
        ss_res += single_mse
    print('residual sum of squares:',ss_res)
    

    for i in range(0, 200):
        sum_y_true += y_true[i]

    avg_y_true = sum_y_true/len(dataset)
    #print(avg_y_true) #3.03759044807835

    for i in range(0, 200):
        tot_sum = (y_true[i] - avg_y_true)**2
        #print(tot_sum)
        ss_total += tot_sum

    #print(ss_total)

    #R2 error
    r2 = 1 - (ss_res/ss_total)
    print('accuracy', r2*100)
    #print('true val', y_true)
    #print('pred', y_pred)

    #return r2

    #return mean_squared_error(y_true, y_pred,multioutput='uniform_average')
    '''y_pred = regressor.predict([[rating,wins,time_diff]])'''
    #print(y_true)
    #print(y_pred)
