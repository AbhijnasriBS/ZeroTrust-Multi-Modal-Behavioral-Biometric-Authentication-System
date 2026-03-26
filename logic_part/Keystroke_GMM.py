#keystroke_GMM.py

from sklearn.mixture import GaussianMixture
import pandas 
from EER_GMM import evaluateEERGMM
import numpy as np
import warnings
warnings.filterwarnings("ignore")

class GMMDetector:
#the training(), testing() and evaluateEERGMM() function change, rest all is same.

    def __init__(self, subjects):
        self.user_scores = []
        self.imposter_scores = []
        self.mean_vector = []
        self.subjects = subjects
        
    def training(self):
        self.gmm = GaussianMixture(n_components = 2, covariance_type = 'diag', 
                        verbose = False )
        self.gmm.fit(self.train)
 
    def testing(self):
        for i in range(self.test_genuine.shape[0]):
            j = [self.test_genuine.iloc[i].values]
            cur_score = self.gmm.score(j)
            self.user_scores.append(cur_score)
 
        for i in range(self.test_imposter.shape[0]):
            j = [self.test_imposter.iloc[i].values]
            cur_score = self.gmm.score(j)
            self.imposter_scores.append(cur_score)
 
    def evaluate(self):
        eers = []
 
        for subject in subjects:        
            genuine_user_data = data.loc[data.subject == "saksham", \
                                         "H.period":"UD.l.Return"]
            imposter_data = data.loc[data.subject != subject, :]
            
            self.train = genuine_user_data[-1:]
            self.test_genuine = genuine_user_data[:20]
            self.test_imposter = imposter_data.groupby("subject"). \
                                 head(20).loc[:, "H.period":"UD.l.Return"]
 
            self.training()
            self.testing()
            eers.append(evaluateEERGMM(self.user_scores, \
                                     self.imposter_scores))
        return np.mean(eers)

path = "D:/me lazy/SDD/others/key specific/User-Verification-based-on-Keystroke-Dynamics-master/keystroke.trial.csv" 
data = pandas.read_csv(path)
subjects = data["subject"].unique()
print ("average EER for GMM detector:")
print(GMMDetector(subjects).evaluate())

