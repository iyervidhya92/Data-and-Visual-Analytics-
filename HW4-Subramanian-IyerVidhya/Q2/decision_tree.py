from util import entropy, information_gain, partition_classes
import numpy as np 
import ast

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        self.tree = []
        #self.tree = {}


    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        self.tree = self.make_tree(X,y)


    def make_classify(self, tree, record):
        index, split_value = tree.keys()[0]
        
        if isinstance(record[index], str): 
            idx = 0 if record[index] == split_value else 1
        else:
            idx = 0 if record[index] <= split_value else 1
        
        final = tree.values()[0][idx]
        
        if type(final) == dict:
            return self.make_classify(final, record)
        else:
            return final


    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
         return self.make_classify(self.tree, record)


    def make_tree(self, X, y):
        
        if len(set(y)) == 1:
            return y[0]
            
        max_info_gain = -1
        index = None
        value = None
        
        X_left, X_right, y_left, y_right = [], [], [], []
                
        for i in range(len(X[0])):
            
            current = []
            for row in X:
                current.append(row[i])
                        
            for split_val in set(current):
                X_left_t, X_right_t, y_left_t, y_right_t = partition_classes(X, y, i, split_val)
                info_gain = information_gain(y, [y_left_t,y_right_t])
                if info_gain > max_info_gain:
                    max_info_gain = info_gain
                    index, value = i, split_val
                    X_left, X_right, y_left, y_right = X_left_t, X_right_t, y_left_t, y_right_t
        node_data = (index, value)
        return  {node_data: [self.make_tree(X_left, y_left), self.make_tree(X_right, y_right)]}
