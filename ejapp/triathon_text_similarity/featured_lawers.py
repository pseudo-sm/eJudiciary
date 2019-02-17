import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

rating = np.random.random(20)
print(rating)

win_list = []

for i in rating:

    if i > 0.7 :
        win = np.random.randint(6, 8)
        win_list.append(win)
        continue
    if i > 0.5 and i < 0.7:
        win2 = np.random.randint(4, 6)
        win_list.append(win2)
        continue
    elif i < 0.5 and i > 0.2:
        win3 = np.random.randint(2, 4)
        win_list.append(win3)
        continue
    else :
        win4 = np.random.randint(0, 2)
        win_list.append(win4)
        continue

print(win_list)

df = pd.DataFrame()
df['Ratings'] = rating
df['Wins'] = win_list
df['Score'] = [0.89,1.99,4.7,1.6,3.67,0.2,1.1,3.889,0.12,2.1,3.2,4,1.3,1.5,1.44,1.05,0.6,1.32,4.9,3.2]
df.to_csv('lawers.csv', index=False, encoding='utf8')

dataset = pd.read_csv('./lawers.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 2].values

#learning
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X,y)

#prediction
y_pred = regressor.predict([[0.9,7]])
print(y_pred)

plt.scatter(dataset['Wins'], y, color = 'r')
plt.plot(dataset['Wins'], regressor.predict(X) , label = 'b')
plt.title('Wins vs Score')
plt.xlabel('wins')
plt.ylabel('score')
plt.show()