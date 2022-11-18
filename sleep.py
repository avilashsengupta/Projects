import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

dataset = pd.read_csv('sleep.csv')
work_stress_level = dataset.iloc[:,1:3].values
sleep_hour_require = dataset.iloc[:,-1].values
index = [str(i) for i in list(dataset['Index'])]

reg = LinearRegression()
reg.fit(work_stress_level, sleep_hour_require)
LinearRegression(copy_X=True, fit_intercept=True, normalize=False)
predicted_sleep = reg.predict(work_stress_level)
accuracy = round(r2_score(sleep_hour_require, predicted_sleep),4)

plt.title('Hours of Sleep Prediction [ Accuracy '+str(accuracy*100)+' ]')
plt.scatter(index, list(dataset['Daily_Sleep_Required']), color='limegreen')
plt.plot(index, predicted_sleep, color='royalblue', linewidth=3)
plt.xlabel('Index values of Stress & Work Hour')
plt.ylabel('Hours of Sleep a Day')
plt.legend(['Predicted Sleep Hour','Given Sleep Hour'], loc='upper left')
plt.show()
