#import libraries
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

#import dataset
URL="https://raw.githubusercontent.com/AdiPersonalWorks/Random/master/student_scores%20-%20student_scores.csv"
df=pd.read_csv(URL)
print("Data imported successfully")
#inspect the data
print(df.shape)
print(df.head())
print(df.describe())
Scores=df["Scores"]
Hours=df["Hours"]
avg_scores=Scores.mean()
avg_hours=Hours.mean()
print("On Average a student studying:", avg_hours, " will attain an average score of :", avg_scores)
#Correlation between variablesavg_hours
df.corr()
print(" Correlation between hours and scores is 0.976191")

#Graphical Visualization of Data 
# Plotting the distribution of scores
df.plot(x='Hours', y='Scores',style='o')  
plt.title('Hours vs Percentage Score') 
plt.grid(True)
plt.xlabel('Hours Studied')  
plt.ylabel('Percentage Score')  
plt.show()
#Inference
print(" Positive linear relation between the number of hours studied and percentage of score.")

#Preparing Data for Modelling
X = df.iloc[:, :-1].values  
y = df.iloc[:, 1].values
#Training the model
from sklearn.model_selection import train_test_split
##Split the data into train and test model
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.20,random_state=0)

#Fit the model
from sklearn.linear_model import LinearRegression
linreg = LinearRegression()
linreg.fit(X_train, y_train)
print("Training Complete")
print('Intercept: ',linreg.intercept_)

# Plotting the regression line
line = linreg.coef_*X+linreg.intercept_

# Plotting for the test data
plt.scatter(X, y)
plt.plot(X, line,color = 'green')
plt.show()
#Predict the model
print(X_test) # Testing data - In Hours
y_pred = linreg.predict(X_test) # Predicting the scores
# Comparing Actual vs Predicted
df1 = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})  
print(df1)
# testing with  own data
hours = 9.25
own_pred = linreg.predict([[hours]])
print("No of Hours of Study = {}".format(hours))
print("Predicted Score = {}".format(own_pred[0]))

#Evaluating the model
from sklearn import metrics  
print('Mean Absolute Error:', 
      metrics.mean_absolute_error(y_test, y_pred))
print("Residual sum of squares(MSE): %.2f" % np.mean((y_pred - y_test) ** 2))
MSE=np.mean((y_pred - y_test) ** 2)
print("Root mean squares error (RMSE): %.2f" % np.sqrt(MSE))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % linreg.score(X_test, y_test))
print("Mean absolute error: %.2f" % np.mean(np.absolute(y_pred - y_test)))
print("R2-score: %.2f" % metrics.r2_score(y_pred ,y_test))
print(linreg.score(X_test,y_test)*100,'% Prediction Accuracy') 
