from trace_classifier import TraceClassifier
import numpy as np
import sqlite3
import os

os.remove(r"C:\personal-git\Thesis\ThesisScripts\data\DerivativeStructureTest\testTrigo\test_method_traces.log")
# with open(PATH, "r") as f:
#     classifier = TraceClassifier()
#     np_array_vec = [np.fromstring(",".join(vector.split(',')[1:])[:-1], sep=",") for vector in f]
#     classifier.fit(np_array_vec)