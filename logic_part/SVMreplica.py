from sklearn.svm import OneClassSVM
import numpy as np
np.set_printoptions(suppress = True)
import pandas
from sklearn.metrics import roc_curve

def evaluateEER(user_scores):
    labels = [0]*len(user_scores) 
    fpr, tpr, _ = roc_curve(labels, user_scores)
    #print('fpr','tpr','thres',fpr,tpr,thresholds)
    missrates = 1 - tpr
    farates = fpr
#    array = np.zeros((123,3))
#    array[:,0] = missrates
#    array[:,1] = farates
#    array[:,2] = thresholds
#    print array
    dists = missrates - farates
    idx1 = np.argmin(dists[dists >= 0])
    idx2 = np.argmax(dists[dists < 0])
    x = [missrates[idx1], farates[idx1]]
    y = [missrates[idx2], farates[idx2]]
    a = ( x[0] - x[1] ) / ( y[1] - x[1] - y[0] + x[0] )
    eer = x[0] + a * ( y[0] - x[0] )
    return eer

class SVMDetector:
#just the training() function changes, rest all remains same.

    def __init__(self, subjects):
        self.u_scores = []
        self.mean_vector = []
        self.subjects = subjects
        
    
    def training(self):
        self.clf = OneClassSVM(kernel='rbf',gamma=26)
        self.clf.fit(self.train)
 
    def testing(self):
        self.u_scores = -self.clf.decision_function(self.test_genuine)
        self.u_scores = list(self.u_scores)
        #print(self.u_scores)
        #print(len(self.i_scores[0]))
        
 #remove imposter   
    def evaluate(self):
        eers = []
        
        for subject in subjects:        
            genuine_user_data = data.loc[data.subject == subject, \
                                         "H.period":"H.Return"]
            imposter_data = data.loc[data.subject != subject, :]    
            self.train = genuine_user_data[:1]
            self.test_genuine = genuine_user_data[1:]
            #total - selected genuine ,,,,, first five of every imposter displayed 
            print(genuine_user_data[:1])
            self.training()
            self.testing()
            eers.append(evaluateEER(self.u_scores))

        return np.mean(eers)
        #returns the average of array elements

path = "D:/me lazy/SDD/others/key specific/User-Verification-based-on-Keystroke-Dynamics-master/key1.csv" 
data = pandas.read_csv(path)
subjects = data["subject"]
print("average EER for SVM detector:")
print(SVMDetector(subjects).evaluate())
