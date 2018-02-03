from collections import defaultdict
from trace_classifier import TraceClassifier
import random
import sqlite3
import os

# consts
BUGDB_PATH = "C:\\personal-git\\Thesis\\ThesisScripts\\bugdbs\\1\\"
NULL_MAGIC_NUMBER = "0"
MIN_SIZE_PER_METHOD = 1000
REMOVE_STATIC = "STATIC,"
REMOVE_VOID = ",VOID"
REPLACE_NULL = "NULL"
NULL_MAGIC_NUMBER = "0"
FAULTY_METHOD_LIKE = '%DerivativeStructure.divide%'

# setup
conn = sqlite3.connect(BUGDB_PATH + "tracedb.sqlite")
random.seed(7)

## make sure that buggy method has enough samples
print("Validation")
cur = conn.cursor()
mid_count_tuple = cur.execute(f"""select mid, count(mid) 
                                from traces 
                                inner join methods 
                                where traces.mid = methods.method_id and methods.method_name like '{FAULTY_METHOD_LIKE}'""")
faulty_method_count = list(mid_count_tuple)[0][1]
if faulty_method_count < MIN_SIZE_PER_METHOD:
    raise ValueError(f"faulty method: '{FAULTY_METHOD_LIKE}' does not have the minimum allowed number of traces: {MIN_SIZE_PER_METHOD}")

trainsets_dir_path = BUGDB_PATH + "\\trainsets"
if not os.path.exists(trainsets_dir_path):
    os.makedirs(trainsets_dir_path)

print("Create individual datasets")
cur = conn.cursor()
all_mids = cur.execute("select distinct mid from traces")
for mid in all_mids:
    cur = conn.cursor()
    mid = mid[0]
    vectors = cur.execute(f"select replace(replace(replace(vector, '{REMOVE_STATIC}', ''), '{REMOVE_VOID}', ''), '{REPLACE_NULL}', '{NULL_MAGIC_NUMBER}') from traces where mid='{mid}'")
    with open(trainsets_dir_path + f"\\trainset_{mid}.csv", "w") as trainset_file:
        for v in vectors:
            trainset_file.write(v[0] + '\n')
    