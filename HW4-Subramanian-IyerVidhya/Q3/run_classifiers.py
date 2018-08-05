## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to recognize seizure from EEG brain wave signals

import numpy as np
import pandas as pd
import time 

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize

######################################### Reading and Splitting the Data ###############################################

# Read in all the data.
data = pd.read_csv('seizure_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data. DO NOT CHANGE.
random_state = 100 # DO NOT CHANGE

# XXX
# TODO: Split each of the features and labels arrays into 70% training set and
#       30% testing set (create 4 new arrays). Call them x_train, x_test, y_train and y_test.
#       Use the train_test_split method in sklearn with the parameter 'shuffle' set to true 
#       and the 'random_state' set to 100.
# XXX
X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.30, random_state = random_state);


# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
# XXX
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
# XXX
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Use y_predict.round() to get 1 or 0 as the output.
# XXX
print("LinearRegression")
print("Training")
y_true, y_pred = y_train, linear_model.predict(X_train).round()
acc_score = accuracy_score(y_true, y_pred)
print(acc_score)

print("Testing")
y_true, y_pred = y_test, linear_model.predict(X_test).round()
acc_score = accuracy_score(y_true, y_pred)
print(acc_score)

# ############################################### Multi Layer Perceptron #################################################
# XXX
# TODO: Create an MLPClassifier and train it.
# XXX
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=random_state)
clf.fit(X_train,  y_train)

# XXX
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
print("MLPClassifier")
print("Training")
y_true, y_pred = y_train, clf.predict(X_train).round()
acc_score = accuracy_score(y_true, y_pred)
print(acc_score)
print("Testing")
y_true, y_pred = y_test, clf.predict(X_test).round()
acc_score = accuracy_score(y_true, y_pred)
print(acc_score)


# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
# XXX
random_model = RandomForestClassifier()
random_model.fit(X_train, y_train)
# XXX
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
print("RandomForestClassifier")
print("Training")
y_true, y_pred = y_train, random_model.predict(X_train).round()
acc_score = accuracy_score(y_true, y_pred)
print(acc_score)
print("Testing")
y_true, y_pred = y_test, random_model.predict(X_test).round()
acc_score = accuracy_score(y_true, y_pred)
print(acc_score)

# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
tuned_parameters = {'n_estimators':[10,20,30], 'max_depth':[10,20,30]}

clf = GridSearchCV(RandomForestClassifier(), tuned_parameters, cv=10)
clf.fit(X_train, y_train)

print("Best parameters set found on development set:")
print(clf.best_params_)
print(clf.best_score_)

print("Testing")
y_true, y_pred = y_test, clf.predict(X_test).round()
acc_score = accuracy_score(y_true, y_pred)
print(acc_score)

# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Create a SVC classifier and train it.
# XXX
model = SVC()
model.fit(X_train, y_train)

# XXX
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
print("SVC")
print("Training")
y_true, y_pred = y_train, model.predict(X_train).round()
acc_score = accuracy_score(y_true, y_pred)
print(acc_score)
print("Testing")
y_true, y_pred = y_test, model.predict(X_test).round()
acc_score = accuracy_score(y_true, y_pred)
print(acc_score)

# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
X_train_norm = normalize(X_train, norm='l2')
X_test_norm = normalize(X_test, norm='l2')

tuned_parameters = {'kernel':('linear', 'rbf'), 'C':[0.0001, 0.1, 10]}

clf = GridSearchCV(SVC(), tuned_parameters, cv=10)
clf.fit(X_train_norm, y_train)

print("Best parameters set found on development set:")
print(clf.best_params_)
print(clf.best_score_)

print("Testing")
y_true, y_pred = y_test, clf.predict(X_test_norm).round()
acc_score = accuracy_score(y_true, y_pred)
print(acc_score)

# XXX 
# ########## PART C ######### 
# TODO: Print your CV's highest mean testing accuracy and its corresponding mean training accuracy and mean fit time.
# 		State them in report.txt.
# XXX
print("Mean test scores")
maxVal = max(clf.cv_results_['mean_test_score'])
index = clf.cv_results_['mean_test_score'].tolist().index(maxVal)
print(maxVal)
print(clf.cv_results_['mean_train_score'][index])
print(clf.cv_results_['mean_fit_time'][index])
