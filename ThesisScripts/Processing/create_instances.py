import random
import sqlite3

BUGDB_PATH = "C:\\personal-git\\Thesis\\ThesisScripts\\bugdbs\\1\\"
REMOVE_STATIC = "STATIC,"
REMOVE_VOID = ",VOID"
REPLACE_NULL = "NULL"
NULL_MAGIC_NUMBER = "0"
FAULTY_METHOD_LIKE = '%DerivativeStructure.divide%'

INSTANCES_PATH = BUGDB_PATH + "instances\\"
conn = sqlite3.connect(BUGDB_PATH + "tracedb.sqlite")
random.seed(7)

#count number of fail tests
curr = conn.cursor()
fail_tmids = curr.execute("""select tmid from outcomes where outcomes.is_faulty = 1""")
fail_tmids = [record[0] for record in fail_tmids]
#count number of succ tests
curr = conn.cursor()
succ_tmids = curr.execute("""select tmid from outcomes where outcomes.is_faulty = 0""")
succ_tmids = [record[0] for record in succ_tmids]

##get all methods
#faulty methods
cur = conn.cursor()
faulty_mids = cur.execute(f"""select distinct traces.mid
                                from traces 
                                inner join methods 
                                where traces.mid = methods.method_id and methods.method_name like '{FAULTY_METHOD_LIKE}'""")
faulty_mids = set([record[0] for record in faulty_mids])
#healthy methods
curr = conn.cursor()
all_mids = curr.execute("""select distinct traces.mid from traces""")
all_mids = set([record[0] for record in all_mids])
healthy_mids = all_mids.difference(faulty_mids)

print("Creating Matrix")
MATRIX_TESTS = [10, 20, 30, 40, 50]
MATRIX_METHODS = [10, 20, 30, 40, 50]
for test_count in MATRIX_TESTS:
    for method_count in MATRIX_METHODS:
        for idx in range(10):
            ### sample succ tmids
            # complete the matrix test size with remaining healthy test methods
            remainder_test_size = test_count - len(fail_tmids)
            # sample ramaining successful test out of size left
            remainder_succ_tmids = random.sample(succ_tmids, remainder_test_size)
            # unify all
            all_relevant_tmids = remainder_succ_tmids + fail_tmids
            ### sample relevant healthy mids [we already computed before all_mids, faulty_mids and healthy_mids]
            # tmids as a long comma separated list
            relevant_tmids_str = [f"'{tmid}'" for tmid in all_relevant_tmids]
            relevant_tmids_str = ','.join(relevant_tmids_str)
            # get all healthy mids from the chosen tmids
            curr = conn.cursor()
            all_healthy_mids_from_tids = curr.execute(F"""select distinct traces.mid
                                                    from traces
                                                    inner join outcomes
                                                    on traces.tmid=outcomes.tmid
                                                    inner join methods
                                                    on traces.mid = methods.method_id
                                                    where traces.tmid in ({relevant_tmids_str})
                                                    and methods.method_name not like '{FAULTY_METHOD_LIKE}'
                                                    """)
            all_healthy_mids_from_tids = set([record[0] for record in all_healthy_mids_from_tids])
            # calc size of healthy mids sample
            remainder_healthy_methods_size = method_count - len(faulty_mids)
            # sample the remainder
            remainder_healthy_methods = random.sample(all_healthy_mids_from_tids, remainder_healthy_methods_size)
            # unify all
            all_relevant_mids = remainder_healthy_methods + fail_tmids
            ## now we have all_relevant_tmids & all_relevant_mids
            # mids as a long comma separated list
            all_relevant_mids_str = [f"'{mid}'" for mid in all_relevant_mids]
            all_relevant_mids_str = ','.join(all_relevant_mids_str)
            # get all traces in the form of (tmid, mid, vector, is_faulty)
            curr = conn.cursor()
            all_relevant_traces = curr.execute(F"""select distinct traces.tmid,
                                                    traces.mid,
                                                    replace(replace(replace(traces.vector, '{REMOVE_STATIC}', ''), '{REMOVE_VOID}', ''), '{REPLACE_NULL}', '{NULL_MAGIC_NUMBER}'),
                                                    outcomes.is_faulty
                                                    from traces
                                                    inner join outcomes
                                                    on traces.tmid = outcomes.tmid
                                                    where traces.tmid in ({relevant_tmids_str})
                                                    and traces.mid in ({all_relevant_mids_str})
                                                    """)
            ### create CSV file
            x = 1
            ## create file json
            #create A and E
            #key already in A - this means multiple invocations of the same
            #method during the same test. write all and choose max in diagnoser
            # ROWS = dict()
            # for (tmid, mid, vector, is_faulty) in remainder_succ_fail_records:
            #     if mid not in ROWS[tmid]:
            #         ROWS[tmid][mid] = []
            #     ROWS[tmid][mid]["vector"] = vector
            #     ROWS[tmid][mid]["is_faulty"] = is_faulty
            # with open(BUGDB_PATH+f"instance_{size}_{idx}.json", "w") as instance_file:
            #     json.dump(ROWS, instance_file)