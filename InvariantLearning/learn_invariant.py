""" Using scikit-learn lib """
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, roc_auc_score
import pandas as pd

def main():
    """ Synthesise method invariant """
    #consts
    features = 3
    classindex = features
    
    #create the training & test sets, skipping the header row with [1:]
    #dataframe = pd.read_csv(r'..\MethodsData\25-03-2017\TragetCalculator_Calculator_Add.txt')
    dataframe = pd.read_csv(r'TragetCalculator_Calculator_Add.txt')
    msk = np.random.rand(len(dataframe)) < 0.7 #pylint: disable=no-member
    train = dataframe[msk]
    test = dataframe[~msk]
    train_data = train.values
    test_actual_classes = test.values
    test_actual_classes = test_actual_classes[0:, classindex]
    test_data = test.values
    test_data = test_data[0:, 0:classindex]
    model = RandomForestClassifier(n_estimators=10)
    model = model.fit(train_data[0:, 0:classindex], train_data[0:, classindex])
    test_predicted_classes = model.predict(test_data)
    #result = np.c_[test, output]
    #prediction_data = pd.DataFrame(result, columns=['Arg1', 'Arg2', 'Output'])

    accuracy = accuracy_score(test_actual_classes, test_predicted_classes, normalize=True)
    precision = precision_score(test_actual_classes, test_predicted_classes)
    #auc = roc_auc_score(test_actual_classes, test_predicted_classes)
    print("Accuracy: The precent of records that were predicted correctly")
    print(accuracy)
    print("Precision: (Tpos / (Tpos + Fpos)) - The ability not to label negative samples as positive")
    print(precision)
    #print("AUC:")
    #print(auc)

if __name__ == "__main__":
    main()
