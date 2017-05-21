__author__ = 'amir'

import Staccato
import Diagnosis

import math
import TF
import random
import csv
import os
import ast
prior_p = 0.05

class Barinel:

    def __init__(self):
        self.M_matrix = []
        self.b_matrix = []
        self.e_vector = []
        self.diagnoses = []


    def set_matrix_bMatrix_error(self, M, bMatrix, e):
        self.M_matrix = M
        self.b_matrix = bMatrix
        self.e_vector = e

    def generate_probs(self):
        new_diagnoses = []
        probs_sum = 0.0
        for diag in self.diagnoses:
            # Barinel's:
            # dk = math.pow(prior_p,len(diag.get_diag())) #assuming same prior prob. for every component.
            # tf = TF.TF(self.M_matrix,self.e_vector,diag.get_diag())
            # e_dk = tf.maximize()
            # diag.probability = e_dk * dk #temporary probability
            # Ori's:
            total_diag_prob = 1
            for comp in diag.diagnosis:
                comp_prob_acc = 1
                for i, observation in enumerate(self.M_matrix):
                    if observation[comp] == 0:  # component didn't take part in test
                        continue
                    if self.e_vector[i] == 0:  # test didn't fail
                        comp_prob_acc *= 1 - self.b_matrix[i][comp]
                    else:  # test failed
                        comp_prob_acc *= self.b_matrix[i][comp]
                total_diag_prob *= comp_prob_acc
            diag.probability = total_diag_prob
            probs_sum += diag.probability
        for diag in self.diagnoses: #normalizing
            temp_prob = 0
            if probs_sum != 0:
                temp_prob = diag.get_prob() / probs_sum
            diag.probability = temp_prob
            new_diagnoses.append(diag)
        self.diagnoses = new_diagnoses


    def run(self):
        #initialize
        self.diagnoses = []
        diags = Staccato.Staccato().run(self.M_matrix, self.e_vector)
        for  diag in diags:
            d=Diagnosis.Diagnosis()
            d.diagnosis=diag
            self.diagnoses.append(d)
        #generate probabilities
        self.generate_probs()

        return self.diagnoses

def read_gt_and_comps(project_name, folder_name, test_num, test_iter):
    in_file = os.path.join(os.path.dirname(__file__), "DB\\samples\\"+project_name+"\\"+folder_name+"\\bugs_Files\\"+str(test_num)+'_'+str(test_iter)+'.txt')
    with open(in_file,"r") as in_file:
        lines = in_file.read().split('\n')
        comps = '[' + lines[1].strip() + ']'
        comps = ast.literal_eval(comps)
        gt = '[' + lines[3].strip() + ']'
        gt = ast.literal_eval(gt)
    return (gt, comps)

def get_gt(project_name, folder_name, test_num, test_iter):
    (gt, comps) = read_gt_and_comps(project_name, folder_name, test_num, test_iter)
    return gt

def proc_synthetic_matrix(lines,noise,test_num,test_iter, project_name, folder_name):
    #remove probs lines
    lines = lines[1:]
    comp_num = len(lines[0])-1
    error_vec_col_idx = comp_num
    error_vector_per_obs = [int(l[error_vec_col_idx]) for l in lines]
    observations_num = len(lines)
    nlines = [ [ '0' for _ in range(comp_num) ] + [ '0' for _ in range(comp_num) ] + [ '0' ] for _ in range(observations_num) ]
    #copy a's and errors
    for obs_idx, obs in enumerate(lines):
        nlines[obs_idx][comp_num*2] = error_vector_per_obs[obs_idx]
        for c_i in range(comp_num):
            nlines[obs_idx][c_i*2] = lines[obs_idx][c_i]
    nlines = nlines
    #create b's
    for obs_idx, obs in enumerate(lines):
        if error_vector_per_obs[obs_idx] == 0: #no error occured at all
            continue
        for c_i in range(comp_num):
            if obs[c_i] == '0': #comp didn't participate
                continue
            gt = get_gt(project_name, folder_name, test_num, test_iter)
            if c_i in gt:
                nlines[obs_idx][c_i*2 + 1] = str(1 - noise)
            else:
                nlines[obs_idx][c_i*2 + 1] = str(0 + noise)
    return nlines

def load_file_with_header(file, noise, test_num, test_iter, project_name, folder_name):
    with open(file,"r") as f:
        lines = list(csv.reader(f))
        lines = proc_synthetic_matrix(lines, noise, test_num, test_iter, project_name, folder_name)
        comps_num = int((len(lines[0])-1)/2)
        error_vec_col_idx = comps_num * 2
        tests = lines[0:]
        erorr_vector = [int(t[error_vec_col_idx]) for t in tests]
        Matrix = [0 for t in tests]
        bMatrix = [0 for t in tests]
        for idx, t in enumerate(tests):
            Matrix[idx] = [int(elm) for elm in t[:error_vec_col_idx:2]] #a matrix
            bMatrix[idx] = [float(elm) for elm in t[1:error_vec_col_idx:2]] #b matrix
        ans = Barinel()
        ans.set_matrix_bMatrix_error(Matrix, bMatrix, erorr_vector)
        return ans



def test(matrix_file, out_file,  noise, test_num, test_iter, project_name, folder_name):
    bar = load_file_with_header(matrix_file, noise, test_num, test_iter, project_name, folder_name)
    diags = bar.run()
    sorted_diags = sorted(diags, key=lambda d: d.probability, reverse=True)
    with open(out_file, "w") as f:
        f.write(str(sorted_diags))

if __name__=="__main__":
    file_name_template = '{0}_uniform_{1}.csv'
    out_file_name_template = '{0}_usingb_{2}_{1}.csv'
    project_names = [ "ant", "cdt", "orient", "poi" ]
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
        for test_num in range(10, 50, 10):
            # print('start test_num: '+str(test_num))
            for folder_name in project_folders:
                # print('start folder: '+str(folder_name))
                for test_iter in project_range:
                    file_name = file_name_template.format(test_num, test_iter)
                    matrix_file = os.path.join(os.path.dirname(__file__), "DB\\samples\\{2}\\{1}\\barinel\\{0}")
                    out_file = os.path.join(os.path.dirname(__file__), "DB\\samples\\{2}\\{1}\\out\\DIFG_check_{0}")
                    noises = [0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50]
                    for noise in noises:
                        noisestr = str(int(noise * 100))
                        if len(noisestr) is 1:
                            noisestr = '0'+noisestr
                        out_file_name = out_file_name_template.format(test_num, test_iter, noisestr)
                        input_fname = matrix_file.format(file_name, folder_name, project_name)
                        out_fname = out_file.format(out_file_name, folder_name, project_name)
                        print("=================================")
                        print("working on: " + input_fname)
                        print("output to:" + out_fname)
                        test(input_fname, out_fname, noise, test_num, test_iter, project_name, folder_name)
    print("done")
    # test(matrix_file.format('all0'), out_file.format('all0'))
    # test(matrix_file.format('all005'), out_file.format('all005'))
    # test(matrix_file.format('all020'), out_file.format('all020'))
    # test(matrix_file.format('all020'), out_file.format('all030'))
    # test(matrix_file.format('choose_best0'), out_file.format('choose_best0'))
    # test(matrix_file.format('choose_best005'), out_file.format('choose_best005'))
    # test(matrix_file.format('choose_best020'), out_file.format('choose_best020'))
    # test(matrix_file.format('choose_best030'), out_file.format('choose_best030'))
    # test(matrix_file.format('choose_better0'), out_file.format('choose_better0'))
    # test(matrix_file.format('choose_better005'), out_file.format('choose_better005'))
    # test(matrix_file.format('choose_better020'), out_file.format('choose_better020'))
    # test(matrix_file.format('choose_better030'), out_file.format('choose_better030'))
    # test(matrix_file.format('all'), out_file.format('all'))
    # test(matrix_file.format('s0'), out_file.format('s0'))
    # test(matrix_file.format('choose_worse'), out_file.format('choose_worse'))
    # test(matrix_file.format('choose_better'), out_file.format('choose_better'))
    # test(matrix_file.format('choose_best'), out_file.format('choose_best'))
