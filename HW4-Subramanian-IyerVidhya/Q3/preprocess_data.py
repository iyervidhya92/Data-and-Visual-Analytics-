## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms on the seizure dataset.

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.svm import SVC

######################################### Reading and Splitting the Data ###############################################

# Read in all the data.
data = pd.read_csv('seizure_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100 # DO NOT CHANGE

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the parameter 'shuffle' set to true and the 'random_state' set to 100.
# XXX
X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.30, random_state = random_state);


# ###################################### Without Pre-Processing Data ##################################################
# XXX
# TODO: Fit the SVM Classifier (with the tuned parameters)  on the x_train and y_train data.
# XXX
model = SVC(C=0.0001, kernel='linear')
model.fit(X_train, y_train)

# XXX
# TODO: Predict the y values for x_test and report the test accuracy using the accuracy_score method.
# XXX

y_true, y_pred = y_test, model.predict(X_test).round()
acc_score = accuracy_score(y_true, y_pred)
print(acc_score)

# ###################################### With Data Pre-Processing ##################################################
# XXX
# TODO: Standardize or normalize x_train and x_test using either StandardScalar or normalize().
# Call the processed data x_train_p and x_test_p.
# XXX
scaler = StandardScaler().fit(X_train)
x_train_p = scaler.transform(X_train)
x_test_p = scaler.transform(X_test)


# XXX
# TODO: Fit the SVM Classifier (with the tuned parameters) on the x_train_p and y_train data.
# XXX

model.fit(x_train_p, y_train)

# XXX
# TODO: Predict the y values for x_test_p and report the test accuracy using the accuracy_score method.
# XXX
y_true_p, y_pred_p = y_test, model.predict(x_test_p)
acc_score_p = accuracy_score(y_true_p, y_pred_p)
print(acc_score_p)