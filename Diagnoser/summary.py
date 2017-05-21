import os
import csv
import json
import ast

def metric_wasted_effort(gt, candidates):
    gt = ast.literal_eval(gt)
    effort = set()
    gt_set = set()
    gt_set.update(gt)
    for (cand, prob) in candidates:
        cand = ast.literal_eval(cand)
        if len(gt_set - effort) is 0:
            break
        for c in cand:
            if len(gt_set - effort) is 0:
                break
            effort.add(c)
    wasted_effort = effort - gt_set
    return len(wasted_effort)

def health_state(gt, comps, candidates):
    gt = ast.literal_eval(gt)
    hs = {}
    comps = ast.literal_eval(comps)
    for c in comps:
        hs[str(c)] = 0
    for (cand, prob) in candidates:
        cand = ast.literal_eval(cand)
        for c in cand:
            hs[str(c)] = hs[str(c)]+float(prob)
    hs_vec = []
    for key, value in hs.items():
        hs_vec.append((key,value))
    hs_vec.sort(key=lambda kv: kv[1], reverse=True)
    hs_vec = list(map(lambda x: (str([int(x[0])]),str(x[1])), hs_vec)) # make every comp singleton
    return hs_vec

def hs_wasted_effort(gt, comps, candidates):
    hs = health_state(gt, comps, candidates)
    return metric_wasted_effort(gt, hs)

def metric_tpfptnfn(gt, comps, candidates):
    gt = ast.literal_eval(gt)
    effort = set()
    gt_set = set()
    gt_set.update(gt)
    comps = ast.literal_eval(comps)
    comps_set = set()
    comps_set.update(comps)
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for (cand, prob) in candidates:
        fprob = float(prob)
        cand = ast.literal_eval(cand)
        cand_set = set()
        cand_set.update(cand)
        for positive in cand_set:
            if positive in gt_set:
                tp += 1 * fprob
            else:
                fp += 1 * fprob
        negatives = comps_set - cand_set
        for neg in negatives:
            if neg not in gt_set:
                tn += 1 * fprob
            else:
                fn += 1 * fprob
    return (tp, fp, tn, fn)

def metric_recall(gt, comps, candidates):
    (tp, fp, tn, fn) = metric_tpfptnfn(gt, comps, candidates)
    return tp / (tp+fn)

def metric_precision(gt, comps, candidates):
    (tp, fp, tn, fn) = metric_tpfptnfn(gt, comps, candidates)
    return tp / (tp+fp)

def proc_file(in_file, out_file, instance_name, project_name):
    with open(in_file,"r") as in_file:
        json_data = []
        ground_truth = ""
        for (idx,line) in enumerate(in_file):
            if idx is 0:
                info_json = json.loads(line.strip())
                ground_truth = info_json['ground_truth']
                comps = info_json['components']
            else:
                json_data.append(json.loads(line.strip()))
    for jdata in json_data:
        we = metric_wasted_effort(ground_truth, jdata['diagnosis'])
        precision = metric_precision(ground_truth, comps, jdata['diagnosis'])
        recall = metric_recall(ground_truth, comps, jdata['diagnosis'])
        hs_we = hs_wasted_effort(ground_truth, comps, jdata['diagnosis'])
        need_headers = False
        algo_name = jdata['algo']
        param = jdata['param']
        if 'uniform' in algo_name:
            algo_name = "barinel"
        elif 'weka_randomForest' in algo_name:
            algo_name = "comp prob"
        elif 'usingb' in algo_name:
            algo_name = "comp/test prob"
        else:
            raise Exception("impossible")
        if not os.path.exists(out_file):
            need_headers = True
        most_or_all = ""
        if 'most' in in_file.name.lower():
            most_or_all = 'most'
        elif 'all' in in_file.name.lower():
            most_or_all = 'all'
        else:
            raise Exception('impossible')
        (test_num, test_iter) = instance_name.split('_')
        with open(out_file, "a") as out:
            if need_headers:
                out.write("algo,noise,project,test #,instance,most or all,wasted effort, precision, recall, HS wasted effort\n")
            out.write(algo_name+','+param+','+project_name+','+test_num+','+test_iter+','+most_or_all+','+str(we)+','+str(precision)+','+str(recall)+','+str(hs_we)+'\n')

def go():
    project_names = ["ant", "cdt", "orient", "poi"]
    for project_name in project_names:
        # print('start project: '+str(project_name))
        project_range = []
        project_folders = []
        if project_name is "ant":
            project_range = range(0,21)
            project_folders = [ "methodsAll864", "methodsMost246" ]
        elif project_name is "cdt":
            project_range = range(0,14)
            project_folders = [ "methodsAll750", "methodsMost750" ]
        elif project_name is "orient":
            project_range = range(0,15)
            project_folders = [ "methodsAll381", "methodsMost557" ]
        elif project_name is "poi":
            project_range = range(0,17)
            project_folders = [ "methodsAll742", "methodsMost556" ]
            # print('start test_num: '+str(test_num))
        for folder_name in project_folders:
            for test_num in range(10, 50, 10):
                # print('start folder: '+str(folder_name))
                for test_iter in project_range:
                    instance_name = project_name+"_"+folder_name+"_"+str(test_num)+"_"+str(test_iter)
                    print(instance_name)
                    instance_name_for_summary = str(test_num)+"_"+str(test_iter)
                    in_file = os.path.join(os.path.dirname(__file__), "DB\\processed_samples\\"+instance_name+".csv")
                    out_file = os.path.join(os.path.dirname(__file__), "DB\\processed_samples_summary\\summary.csv")
                    proc_file(in_file, out_file, instance_name_for_summary, project_name)

go()
