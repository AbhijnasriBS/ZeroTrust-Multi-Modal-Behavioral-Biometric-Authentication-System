#keystroke_ManhattanFiltered.py

from sklearn.svm import OneClassSVM
#unsupervised outliner detection ,, esimate the support of high dimensional distribution
import numpy as np
np.set_printoptions(suppress = True)
#determine how float nos or array or other things displayed
#If True, always print floating point numbers using fixed point notation, in which case numbers equal to zero in the current precision will print as zero.
import pandas
#easy to use data
from EER import evaluateEER

class SVMDetector:
#just the training() function changes, rest all remains same.

    def __init__(self, subjects):
        self.u_scores = []
        self.i_scores = []
        self.mean_vector = []
        self.subjects = subjects
        
    
    def training(self):
        self.clf = OneClassSVM(kernel='rbf',gamma=26)
        print(self.clf)
        self.clf.fit(self.train)
        print(self.clf.fit(self.train))
        #print("lop")

 
    def testing(self):
        self.u_scores = -self.clf.decision_function(self.test_genuine)
        self.i_scores = -self.clf.decision_function(self.test_imposter)
        self.u_scores = list(self.u_scores)
        self.i_scores = list(self.i_scores)
        #print(self.u_scores)
        #print("dog")
        #
        #print(self.i_scores)
        #print("cat")
        
        #print(len(self.i_scores[0]))
        
 # specific .tie5Roanl
    def evaluate(self):
        eers = []
        
        for subject in subjects:        
            genuine_user_data = data.loc[data.subject == "vaibhav", \
                                         "H.period":"UD.l.Return"]
            imposter_data = data.loc[data.subject != "vaibhav", :]
            
            self.train = genuine_user_data[-1:]
            
            self.test_genuine = genuine_user_data[:20]
            self.test_imposter = imposter_data.groupby("subject"). \
                                 head(20).loc[:, "H.period":"UD.l.Return"]
            
            #total - selected genuine ,,,,, first five of every imposter displayed 
            
            #print(genuine_user_data[:200])
            self.training()

            self.testing()

            eers.append(evaluateEER(self.u_scores, \
                                     self.i_scores))
            #print(evaluateEER(self.u_scores, \
            #                         self.i_scores))
            #print(np.mean(eers))
            break
        return np.mean(eers)
        #returns the average of array elements

path = "D:/me lazy/SDD/others/key specific/User-Verification-based-on-Keystroke-Dynamics-master/key1.csv" 
data = pandas.read_csv(path)
subjects = data["subject"].unique()
#print(data["subject"].unique())
print("average EER for SVM detector:")
print(SVMDetector(subjects).evaluate())
