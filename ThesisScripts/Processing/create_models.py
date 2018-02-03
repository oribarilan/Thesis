from trace_classifier import TraceClassifier
import numpy as np
import sqlite3
import os
import pickle
from Utility.progress_bar import ProgressBar

BUGDB_PATH = "C:\\personal-git\\Thesis\\ThesisScripts\\bugdbs\\1\\"
TRAINSETS_DIR_PATH = f"{BUGDB_PATH}trainsets\\"
MODELS_DIR_PATH = f"{BUGDB_PATH}models\\"

if not os.path.exists(MODELS_DIR_PATH):
    os.makedirs(MODELS_DIR_PATH)

trainset_filenames = os.listdir(TRAINSETS_DIR_PATH)
print(f"Modeling {len(trainset_filenames)} files")
# pbar = ProgressBar(len(trainset_filenames))
for trainset_filename in trainset_filenames:
    print(trainset_filename)
    trainset_path = f"{TRAINSETS_DIR_PATH}{trainset_filename}"
    prefix = "trainset_"
    postfix = ".csv"
    guid = trainset_filename[len(prefix):-len(postfix)]
    with open(trainset_path, "r") as f:
        classifier = TraceClassifier()
        trainset = np.loadtxt(f, delimiter=',')
        #transform infinity to max float
        trainset[ trainset > np.finfo(np.float64).max ] = np.finfo(np.float64).max
        if len(trainset.shape) is 1:
            if trainset.shape[0] is 1:
                raise ValueError("trainset has only 1 sample")
            trainset = trainset.reshape(-1,1)
        # pbar.advance(f"({len(trainset)} records)")
        classifier.fit(trainset)
        with open(MODELS_DIR_PATH + f"cls_{guid}.pickle", "wb") as handle:
            pickle.dump(obj=classifier, file=handle)

# path = r"C:\personal-git\Thesis\ThesisScripts\bugdbs\1\trainsets\trainset_11b14902-43f8-486e-9007-e206c1abeb58.csv"
# with open(path, "r") as f:
#     trainset = np.loadtxt(f, delimiter=',')
#     #infinity to max float
#     trainset[ trainset > np.finfo(np.float64).max ] = np.finfo(np.float64).max
#     for idx, vector in enumerate(trainset):
#         for item in vector:
#             if not np.isfinite(item):
#                 print("infinite", idx, item, vector)
#             if np.isnan(item):
#                 print("NAN", idx, item, vector)
#             if not isinstance(item, np.float64) :
#                 print("not float", idx, item, vector)
#     classifier = TraceClassifier()
#     classifier.fit(trainset)  