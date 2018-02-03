'''
'''
import numpy as np
from sklearn import svm

class TraceClassifier(object):
    def __init__(self):
        self.clf = svm.OneClassSVM(nu=0.01, kernel="linear", gamma='auto')

    def fit(self, X):
        self.clf.fit(X)

    def predict_proba(self, X):
        y_pred = self.clf.predict(X)
        #the higher the conf value, the higher the possibility for an exception
        confs = self.clf.decision_function(X[y_pred == -1])
        confs = np.abs(confs) / np.max(np.abs(confs), axis=0)
        return confs
