__author__ = 'amir'

import Staccato
import Diagnosis

import math
import TF
import random
import csv
import os

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

def load_file_with_header( file):
    with open(file,"r") as f:
        lines = list(csv.reader(f))
        comps_num = int((len(lines[0])-1)/2)
        error_vec_col_idx = comps_num * 2
        tests = lines[0:]
        erorr_vector = [int(t[error_vec_col_idx]) for t in tests]
        Matrix = [0 for t in tests]
        bMatrix = [0 for t in tests]
        for idx, t in enumerate(tests):
            Matrix[idx] = [int(elm) for elm in t[:error_vec_col_idx:2]] #a matrix
            bMatrix[idx] = [int(elm) for elm in t[1:error_vec_col_idx:2]] #b matrix
        ans = Barinel()
        ans.set_matrix_bMatrix_error(Matrix, bMatrix, erorr_vector)
        return ans



def test(matrix_file, out_file):
    bar = load_file_with_header(matrix_file)
    diags = bar.run()
    sorted_diags = sorted(diags, key=lambda d: d.probability, reverse=True)
    with open(out_file, "wb") as f:
        f.write(str(sorted_diags))

if __name__=="__main__":
    matrix_file = os.path.join(os.path.dirname(__file__), "planning_example\\{0}.csv")
    out_file = os.path.join(os.path.dirname(__file__), "planning_example\\{0}.txt")
    test(matrix_file.format('withb'), out_file.format('withb'))
    # test(matrix_file.format('all'), out_file.format('all'))
    # test(matrix_file.format('s0'), out_file.format('s0'))
    # test(matrix_file.format('choose_worse'), out_file.format('choose_worse'))
    # test(matrix_file.format('choose_better'), out_file.format('choose_better'))
    # test(matrix_file.format('choose_best'), out_file.format('choose_best'))
