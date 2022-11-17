import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

dataset = pd.read_csv('height_weight.csv')
height = dataset.iloc[:,:1].values
weight = dataset.iloc[:,-1].values
tempx, x, tempy, y = train_test_split(height, weight, test_size=3/7)
plt.title('Height & Weight')
plt.plot(list(dataset['Height']), list(dataset['Weight']), color='royalblue', linewidth=2)
plt.xlabel('height')
plt.ylabel('weight')
plt.show()

reg = LinearRegression()
reg.fit(height, weight)
LinearRegression(copy_X=True, fit_intercept=True, normalize=False)
z = reg.predict(x)
accuracy = round(r2_score(y,z),3)
h = [str(i[0]) for i in x]

plt.title('Weight Prediction [ Accuracy = '+str(accuracy)+' ]')
plt.plot(h, y, color='limegreen', linewidth=2)
plt.plot(h, z, color='royalblue', linewidth=2)
plt.xlabel('height')
plt.ylabel('weight')
plt.legend(['Given Weight','Predicted Weight'], loc='upper left')
plt.show()
