import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score

stock = pd.read_csv('/home/oem/Desktop/Python/Uniqlo(FastRetailing)_2012-2016.csv')
x = stock.iloc[:,1:6].values
y = stock.iloc[:,-1].values
print('x :\n',x)
print('y :',y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
reg = LinearRegression()
reg.fit(x_train, y_train)
LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
y_pred = reg.predict(x_test)

print('y-intercept :',reg.intercept_)
print('coeficient :',reg.coef_)

print('mean squared error :',mean_squared_error(y_test,y_pred))
print('mean error :',np.sqrt(mean_squared_error(y_test,y_pred)))
print('r2 score :',round(r2_score(y_test,y_pred),2))
