import sqlite3
import random
import json
import csv
from collections import defaultdict
from trace_classifier import TraceClassifier
import numpy as np
import uuid
import pickle

# consts
BUGDB_PATH = "C:\\personal-git\\Thesis\\ThesisScripts\\bugdbs\\1\\"
MIN_SIZE_PER_METHOD = 1000
FAULTY_METHOD_LIKE = '%DerivativeStructure.divide%'
NULL_MAGIC_NUMBER = "0"

# setup
conn = sqlite3.connect(BUGDB_PATH + "tracedb.sqlite")
random.seed(7)

## make sure that buggy method has enough samples
print("Validation")
cur = conn.cursor()
mid_count_tuple = cur.execute(f"select mid, count(mid) from traces where mid LIKE '%DerivativeStructure.divide%'")
faulty_method_count = list(mid_count_tuple)[0][1]
if faulty_method_count < MIN_SIZE_PER_METHOD:
    raise ValueError(f"faulty method: '{FAULTY_METHOD_LIKE}' does not have the minimum allowed number of traces: {MIN_SIZE_PER_METHOD}")

## get all records with their result
print("Setting up repository")
#faulty/healthy full records - all of the records in the form of #[('DerivativeStructureTest.testAbs', 'org.apache.commons.numbers.combinatorics.FactorialDouble.create()', 'STATIC,1576861390', 0)]
#failing_tmids_set
curr = conn.cursor()
full_records = cur.execute("select outcomes.tmid, mid, vector, is_faulty from outcomes INNER JOIN traces on outcomes.tmid=traces.tmid")

def vector_to_vecarray_remove_prefix(vector):
    prefix = "STATIC,"
    if vector.startswith(prefix):
        vector = vector[len(prefix):]
    vector = vector.replace("NULL", NULL_MAGIC_NUMBER)
    return vector


print("Split repository to fail/succ, create mid->vecarrays")
fail_full_records = []
succ_full_records = []
fail_tmids_set = set()
succ_tmids_set = set()
nameid_to_guid = dict()
full_records_dict_by_mid = defaultdict(list)
for (tmid, mid, vector, is_faulty) in full_records:
    if tmid not in nameid_to_guid:
        nameid_to_guid[tmid] = str(uuid.uuid4())
    if mid not in nameid_to_guid:
        nameid_to_guid[mid] = str(uuid.uuid4())
    vecarray = vector_to_vecarray_remove_prefix(vector)
    item = (nameid_to_guid[tmid], nameid_to_guid[mid], vecarray, is_faulty)
    full_records_dict_by_mid[nameid_to_guid[mid]].append(vecarray)
    if is_faulty:
        fail_full_records.append(item)
        fail_tmids_set.add(tmid)
    else:
        succ_full_records.append(item)
        succ_tmids_set.add(tmid)
fail_tmids_count = len(fail_tmids_set)

# fail_full_records = [(tmid, mid, vector_to_vecarray_remove_prefix(vector), is_faulty) for (tmid, mid, vector, is_faulty) in full_records_lst if is_faulty]
# succ_full_records = [(tmid, mid, vector_to_vecarray_remove_prefix(vector), is_faulty) for (tmid, mid, vector, is_faulty) in full_records_lst if not is_faulty]
# print("Creating fail/succ sets")
# fail_tmids_set = set([tmid for (tmid, mid, vecarray, is_faulty) in fail_full_records])
# succ_tmids_set = set([tmid for (tmid, mid, vecarray, is_faulty) in succ_full_records])

#region create train sets

# record_list_by_mid = [(mid, vector + "," + str(is_faulty)) for (tmid, mid, vector, is_faulty) in full_records_lst]
# full_records_dict_by_mid = defaultdict(list)
# for mid, vector_with_is_faulty in record_list_by_mid:
#     full_records_dict_by_mid[mid].append(vector_with_is_faulty)
# with open(BUGDB_PATH + f"trainsets.csv", "w") as trainset_file:
#     for mid in full_records_dict_by_mid:
#         for vector_with_is_faulty in full_records_dict_by_mid[mid]:
#             trainset_file.write(mid + ',' + vector_with_is_faulty + '\n')

#endregion

print("Save mapping of tmid and mid to guid")
with open(BUGDB_PATH + "nameid_to_guid_mapping.csv", "w") as mapping_file:
    mapping_file.write("tmid_or_mid,guid\n")
    for nameid in nameid_to_guid:
        mapping_file.write(f"{nameid},{nameid_to_guid[nameid]}\n")

print("Create individual datasets")
for guid in full_records_dict_by_mid:
    with open(BUGDB_PATH + f"trainset_{guid}.csv", "w") as trainset_file:
        for vecarray in full_records_dict_by_mid[guid]:
            trainset_file.write(vecarray + '\n')

models = dict()
for guid in full_records_dict_by_mid:
    print(f"modeling {guid} with {len(full_records_dict_by_mid[guid])} records")
    classifier = TraceClassifier()
    np_array_vec = [np.fromstring(vector, sep=",") for vector in full_records_dict_by_mid[guid]]
    classifier.fit(np_array_vec)
    with open(BUGDB_PATH + f"cls_{guid}.pickle", "wb") as handle:
        pickle.dump(classifier, handle)

# create matrix
print("Creating Matrix")
MATRIX_SIZES = [10, 20, 30, 40, 50]
for size in MATRIX_SIZES:
    for idx in range(10):
        # complete the matrix size with remaining healthy test methods
        remainder_size = size - fail_tmids_count
        # sample ramaining successful test out of size left
        remainder_succ_tmids = random.sample(succ_tmids_set, remainder_size)
        # get all of the remainder records
        remainder_succ_full_records = [(tmid, mid, vector, is_faulty) for (tmid, mid, vector, is_faulty) in succ_full_records if tmid in remainder_succ_tmids]
        ## create file json
        #create A and E
        #key already in A - this means multiple invocations of the same
        #method during the same test. write all and choose max in diagnoser
        ROWS = dict()
        for (tmid, mid, vector, is_faulty) in fail_full_records + remainder_succ_full_records:
            if mid not in ROWS[tmid]:
                ROWS[tmid][mid] = []
            ROWS[tmid][mid]["vector"] = vector
            ROWS[tmid][mid]["is_faulty"] = is_faulty
        with open(BUGDB_PATH+f"instance_{size}_{idx}.json", "w") as instance_file:
            json.dump(ROWS, instance_file)