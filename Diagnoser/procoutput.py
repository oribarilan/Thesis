import os
import csv
import json
import ast

def read_gt_and_comps(project_name, folder_name, test_num, test_iter):
    in_file = os.path.join(os.path.dirname(__file__), "DB\\samples\\"+project_name+"\\"+folder_name+"\\bugs_Files\\"+str(test_num)+'_'+str(test_iter)+'.txt')
    with open(in_file,"r") as in_file:
        lines = in_file.read().split('\n')
        comps = '[' + lines[1].strip() + ']'
        comps = ast.literal_eval(comps)
        gt = '[' + lines[3].strip() + ']'
        gt = ast.literal_eval(gt)
    return (gt, comps)

def get_actual_bugs():
    #ant-methodall864
    actual_bugs = {}
    actual_bugs[10,0] = [0,1]
    actual_bugs[10,1] = [0,1]
    actual_bugs[10,2] = [0,1,2,3]
    actual_bugs[10,3] = [0,1]
    actual_bugs[10,4] = [0]
    actual_bugs[10,5] = [0]
    actual_bugs[10,6] = [0,1,2]
    actual_bugs[10,7] = [0,1]
    actual_bugs[10,8] = [0,1,2,3,4]
    actual_bugs[10,9] = [0,1,2]
    actual_bugs[10,10] = [0,1]
    actual_bugs[10,11] = [0,1,2]
    actual_bugs[10,12] = [0,1,2]
    actual_bugs[10,13] = [0,1,2]
    actual_bugs[10,14] = [0,1,2,3,4,5]
    actual_bugs[10,15] = [0,1,2]
    actual_bugs[10,16] = [0,1,2]
    actual_bugs[10,17] = [0,1]
    actual_bugs[10,18] = [0,1,2,3]
    actual_bugs[10,19] = [0,1]
    actual_bugs[10,20] = [0]

    actual_bugs[20,0] = [0,1]
    actual_bugs[20,1] = [0,1]
    actual_bugs[20,2] = [0,1,2,3,4]
    actual_bugs[20,3] = [0,1,2]
    actual_bugs[20,4] = [0,1]
    actual_bugs[20,5] = [0]
    actual_bugs[20,6] = [0,1,2]
    actual_bugs[20,7] = [0,1]
    actual_bugs[20,8] = [0,1,2,3,4]
    actual_bugs[20,9] = [0,1,2]
    actual_bugs[20,10] = [0,1,2]
    actual_bugs[20,11] = [0,1,2]
    actual_bugs[20,12] = [0,1,2]
    actual_bugs[20,13] = [0,1,2]
    actual_bugs[20,14] = [0,1,2,3,4,5]
    actual_bugs[20,15] = [0,1,2,3]
    actual_bugs[20,16] = [0,1,2,3]
    actual_bugs[20,17] = [0,1,2]
    actual_bugs[20,18] = [0,1,2,3]
    actual_bugs[20,19] = [0,1,2,3]
    actual_bugs[20,20] = [0]

    actual_bugs[30,0] = [0,1]
    actual_bugs[30,1] = [0,1]
    actual_bugs[30,2] = [0,1,2,3,4]
    actual_bugs[30,3] = [0,1,2]
    actual_bugs[30,4] = [0,1]
    actual_bugs[30,5] = [0,1,2]
    actual_bugs[30,6] = [0,1,2]
    actual_bugs[30,7] = [0,1]
    actual_bugs[30,8] = [0,1,2,3,4]
    actual_bugs[30,9] = [0,1,2]
    actual_bugs[30,10] = [0,1,2]
    actual_bugs[30,11] = [0,1,2]
    actual_bugs[30,12] = [0,1,2]
    actual_bugs[30,13] = [0,1,2,3]
    actual_bugs[30,14] = [0,1,2,3,4,5]
    actual_bugs[30,15] = [0,1,2,3]
    actual_bugs[30,16] = [0,1,2,3]
    actual_bugs[30,17] = [0,1,2]
    actual_bugs[30,18] = [0,1,2,3]
    actual_bugs[30,19] = [0,1,2,3,4]
    actual_bugs[30,20] = [0]

    actual_bugs[40,0] = [0,1]
    actual_bugs[40,1] = [0,1]
    actual_bugs[40,2] = [0,1,2,3,4]
    actual_bugs[40,3] = [0,1,2]
    actual_bugs[40,4] = [0,1]
    actual_bugs[40,5] = [0,1,2]
    actual_bugs[40,6] = [0,1,2]
    actual_bugs[40,7] = [0,1]
    actual_bugs[40,8] = [0,1,2,3,4]
    actual_bugs[40,9] = [0,1,2]
    actual_bugs[40,10] = [0,1,2]
    actual_bugs[40,11] = [0,1,2]
    actual_bugs[40,12] = [0,1,2]
    actual_bugs[40,13] = [0,1,2,3]
    actual_bugs[40,14] = [0,1,2,3,4,5]
    actual_bugs[40,15] = [0,1,2,3]
    actual_bugs[40,16] = [0,1,2,3]
    actual_bugs[40,17] = [0,1,2]
    actual_bugs[40,18] = [0,1,2,3]
    actual_bugs[40,19] = [0,1,2,3,4]
    actual_bugs[40,20] = [0]
    return actual_bugs

def get_comps():
    #ant-methodall864
    actual_bugs = {}
    actual_bugs[10,0] = [0,1,2,3,4,5,6,7,8,9,10,11]
    actual_bugs[10,1] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    actual_bugs[10,2] = [0,1,2,3,4,5,6,7,8,9,10]
    actual_bugs[10,3] = [0,1,2,3,4,5]
    actual_bugs[10,4] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    actual_bugs[10,5] = [0,1,2,3,4,5,6,7,8]
    actual_bugs[10,6] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    actual_bugs[10,7] = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    actual_bugs[10,8] = [0,1,2,3,4,5,6,7,8,9,10]
    actual_bugs[10,9] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    actual_bugs[10,10] = [0,1,2,3,4]
    actual_bugs[10,11] = [0,1,2,3,4,5,6,7,8,9,10,11]
    actual_bugs[10,12] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    actual_bugs[10,13] = [0,1,2,3,4,5,6,7,8,9]
    actual_bugs[10,14] = [0,1,2,3,4,5,6,7,8,9,10]
    actual_bugs[10,15] = [0,1,2,3,4,5,6,7,8,9,10]
    actual_bugs[10,16] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    actual_bugs[10,17] = [0,1,2,3,4]
    actual_bugs[10,18] = [0,1,2,3,4,5,6,7]
    actual_bugs[10,19] = [0,1,2,3,4,5]
    actual_bugs[10,20] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]

    actual_bugs[20,0] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    actual_bugs[20,1] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    actual_bugs[20,2] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    actual_bugs[20,3] = [0,1,2,3,4,5,6,7,8,9,10,11]
    actual_bugs[20,4] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61]
    actual_bugs[20,5] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    actual_bugs[20,6] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    actual_bugs[20,7] = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    actual_bugs[20,8] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    actual_bugs[20,9] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    actual_bugs[20,10] = [0,1,2,3,4,5,6,7,8,9,10,11]
    actual_bugs[20,11] = [0,1,2,3,4,5,6,7,8,9,10,11]
    actual_bugs[20,12] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    actual_bugs[20,13] = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    actual_bugs[20,14] = [0,1,2,3,4,5,6,7,8,9,10]
    actual_bugs[20,15] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    actual_bugs[20,16] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    actual_bugs[20,17] = [0,1,2,3,4,5,6,7]
    actual_bugs[20,18] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    actual_bugs[20,19] = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    actual_bugs[20,20] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]

    actual_bugs[30,0] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38]
    actual_bugs[30,1] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    actual_bugs[30,2] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    actual_bugs[30,3] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    actual_bugs[30,4] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67]
    actual_bugs[30,5] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
    actual_bugs[30,6] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    actual_bugs[30,7] = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    actual_bugs[30,8] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    actual_bugs[30,9] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    actual_bugs[30,10] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    actual_bugs[30,11] = [0,1,2,3,4,5,6,7,8,9,10,11]
    actual_bugs[30,12] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    actual_bugs[30,13] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    actual_bugs[30,14] = [0,1,2,3,4,5,6,7,8,9,10]
    actual_bugs[30,15] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    actual_bugs[30,16] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    actual_bugs[30,17] = [0,1,2,3,4,5,6,7,8]
    actual_bugs[30,18] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    actual_bugs[30,19] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    actual_bugs[30,20] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38]

    actual_bugs[40,0] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51]
    actual_bugs[40,1] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    actual_bugs[40,2] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    actual_bugs[40,3] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    actual_bugs[40,4] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67]
    actual_bugs[40,5] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
    actual_bugs[40,6] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    actual_bugs[40,7] = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    actual_bugs[40,8] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    actual_bugs[40,9] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    actual_bugs[40,10] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    actual_bugs[40,11] = [0,1,2,3,4,5,6,7,8,9,10,11]
    actual_bugs[40,12] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    actual_bugs[40,13] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    actual_bugs[40,14] = [0,1,2,3,4,5,6,7,8,9,10]
    actual_bugs[40,15] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    actual_bugs[40,16] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    actual_bugs[40,17] = [0,1,2,3,4,5,6,7,8,9,10]
    actual_bugs[40,18] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    actual_bugs[40,19] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
    actual_bugs[40,20] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38]
    return actual_bugs

def proc_usingb_lambda(self):
    #x in format '[0] P: 0.5'
    self = self[1:]
    arr = self.split(" P: ")
    diag = arr[0]
    prob = arr[1]
    return (diag, prob)

def proc_file(in_file, out_file, instance_name, algo, param, test_num, test_iter, project_name, folder_name):
    need_headers = False
    if not os.path.exists(out_file):
        need_headers = True
    with open(in_file,"r") as in_file:
        lines = list(csv.reader(in_file)) #read values and perform calculations before writing results
    with open(out_file, "a") as f:
        if need_headers:
            info_json = {}
            (gt,comps) = read_gt_and_comps(project_name, folder_name, test_num, test_iter)
            info_json['ground_truth'] = str(gt)
            info_json['components'] = str(comps)
            f.write(json.dumps(info_json)+"\n")
        diag_collection = []
        if 'usingb' not in algo:
            algo_name = algo.format(str(test_num),str(test_iter))
            for line in lines:
                diag_str = '['
                for d in line[:len(line)-2]:
                    diag_str = diag_str + d + ', '
                diag_str = diag_str[:len(diag_str)-2] + ']'
                diag_collection.append((diag_str, line[len(line)-1]))
        else:
            algo_name = algo.format(str(test_num),str(test_iter),str(param))
            lines[0][0] = ' '+lines[0][0][1:]
            last = lines[0][len(lines[0])-1]
            lines[0][len(lines[0])-1] = last[:len(last)-1]
            concat_str = ""
            to_remove_idxs = []
            for idx,l in enumerate(lines[0]):
                if 'P:' in l:
                    if len(concat_str) is not 0:
                        concat_str += ","+l
                        lines[0][idx] = concat_str
                        concat_str = ""
                    continue
                to_remove_idxs.append(idx)
                if '[' in l:
                    concat_str = l
                else:
                    concat_str += ","+l
            for index in sorted(to_remove_idxs, reverse=True):
                del lines[0][index]
            diag_collection = list(map(proc_usingb_lambda, lines[0]))
            for a in lines[0]:
                if a.count('P:') > 1:
                    x=1
        data = {}
        data['algo'] = algo_name
        data['param'] = param
        data['instance_name'] = instance_name
        data['diagnosis'] = diag_collection
        f.write(json.dumps(data)+"\n")

def go():
    project_names = [ "ant", "cdt", "orient", "poi" ]
    algos_and_params = [ ("DIFG_check_{0}_uniform_{1}.csv.csv", ["none"]), ("DIFG_check_{0}_usingb_{2}_{1}.csv", ["00", "05", "10", "15", "20", "30", "40", "50"]), ("DIFG_check_{0}_weka_randomForest{1}.csv.csv", ["none"]) ]
    for (algo,params) in algos_and_params:
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
                        for param in params:
                            if "usingb" in algo:
                                file_name = algo.format(test_num, test_iter, param)
                            else:
                                file_name = algo.format(test_num, test_iter)
                            print(project_name+": "+file_name)
                            in_file = os.path.join(os.path.dirname(__file__), "DB\\samples\\"+project_name+"\\"+folder_name+"\\out\\"+file_name)
                            instance_name = project_name+"_"+folder_name+"_"+str(test_num)+"_"+str(test_iter)
                            out_file = os.path.join(os.path.dirname(__file__), "DB\\processed_samples\\"+instance_name+".csv")
                            proc_file(in_file, out_file, instance_name, algo, param, test_num, test_iter, project_name, folder_name)

go()