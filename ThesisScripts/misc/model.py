import numpy as np
from sklearn import svm
from numpy import genfromtxt
import time
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split

def predict_and_eval(name, X):
    # print("predicting train")
    start = time.time()
    y_pred = clf.predict(X)
    pred_time = time.time()
    n_error = y_pred[y_pred == -1].size
    print("creating confidence matrix using decision function")
    #the higher the conf value, the higher the possibility for an exception
    confs = clf.decision_function(X[y_pred == -1])
    confs = np.abs(confs) / np.max(np.abs(confs), axis=0)
    end = time.time()
    print(f"time took to predict {name} (secs): {pred_time - start}")
    print(f"total samples: {X.shape[0]}")
    print(f"total {name} errors: {n_error}")
    print(f"{name} error %: {n_error / X.shape[0]}")

dataset = genfromtxt(r"C:\personal-git\ThesisScripts\org.apache.commons.math4.ode.sampling.AbstractStepInterpolator.getGlobalCurrentTime().log", delimiter=',')
#removing method name
dataset = dataset[:, 1:]
N = dataset.shape[0]
breakpoint = int(0.7 * N)
np.random.shuffle(dataset)
X_train = dataset[:breakpoint, :]
X_test = dataset[breakpoint:, :]
# fit the model
clf = svm.OneClassSVM(nu=0.01, kernel="linear", gamma='auto')
print("fitting")
start = time.time()
clf.fit(X_train)
end = time.time()
print(str.format("time took to train (secs): {0}", (end - start)))
predict_and_eval("train", X_train)
predict_and_eval("test", X_test)

