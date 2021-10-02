#!/usr/bin/env python
# -*-coding:utf-8 -*-
 
'''
File      :   bayesiannet.py
Created on:   2021/08/03 20:22:34
 
@Author   :   Helder C. R. Oliveira
@Version  :   1.0
@Contact  :   helder.ro@outlook.com
@License  :   (C) Copyright 2021, Helder C. R. Oliveira
@Desc     :   None
'''
 
import pyAgrum as gum
import random
import pandas as pd
import numpy as np
from scipy.stats import norm


class BayesianNet(object):
    def __init__(self) -> None:
        self.r_seed = 101

        # for reproducibility
        # must to run this before create the BN! 
        # Even in the cases where were changed the states names
        gum.initRandom(self.r_seed) 
        random.seed(self.r_seed)

        self.data_initialization()

        self.bn = self.createBN()
        self.populatingCPTs(self.bn)

        print('--> BN created!')

        #gnb.showInference(self.bn, size='45')
        

    def norm_dist(self, x, mean, std_dev):
        dist = norm.pdf(x, loc=mean, scale=std_dev, random_state=self.r_seed)
        dist = dist / np.sum(dist)
        return dist


    def tnorm_dist(self, mean, std_dev, bins=None, size=100000):
        '''TNormal as Fenton's book p.279'''
        d = norm.rvs(size=size, loc=mean, scale=std_dev, random_state=self.r_seed)
        hist,bins = np.histogram(d, bins=bins, density=True, range=(0,1))
        return (hist,bins)


    def data_initialization(self):
        # COVID-19 test accuracy (from Neils paper Table 1)
        df_tests = pd.DataFrame({'Company':['Roche', 'Kurabo', 'Biotech', 
                                            'EuroImmun', 'BioMedomics', 
                                            'OrientBiotech'],
                                'nFP': [5272, 521, 371, 80, 128, 500],
                                'FP': [10, 0, 2, 0, 12, 0],
                                'nFN': [29, 500, 160, 30, 397, 500],
                                'FN':[0, 100, 7, 3, 45, 75]
                                })

        # Neil's paper has wrong names
        df_tests.rename(columns={"nFP": "nP", "nFN": "nN"}, inplace=True)

        # wikipedia is wrong on FPR and FNR
        df_tests['FPR'] = df_tests['FP'] / df_tests['nP']
        df_tests['FNR'] = df_tests['FN'] / df_tests['nN']

        # Specificity: 1 - FPR 
        df_tests['Specificity'] = (1 - df_tests['FPR']) * 100
        # Sensitivity: 1 - FNR
        df_tests['Sensitivity'] = (1 - df_tests['FNR']) * 100

        df_stats = pd.DataFrame({'Mean':df_tests.mean(numeric_only=True), 
                         'Std':df_tests.std(numeric_only=True)})
        df_stats = df_stats.T


        # Diamond Princess: 712 infected out of 3711 (passengers + crew)
        self.NI = 712
        self.NP = 3711
        IPR = self.NI/self.NP
        # print('IPR: %.4f' % (IPR))
        # IPR considered as 0.2 (20%) for calculations in the paper
        IPR = 0.2

        # PTR (based on Neil's paper)
        # P = IPR x (1-FNR) + (1-IPR) x FPR.
        #print('P = IPR x (1-FNR) + (1-IPR) x FPR = %.4f' % (IPR * (1-df_stats['FNR']['Mean']) + (1-IPR) * df_stats['FPR']['Mean']))

        # JIID's report, 2020
        n_symp = [0, 2, 25, 27, 19, 28, 76, 95, 27, 2]
        n_asymp = [1, 3, 3, 7, 8, 31, 101, 139, 25, 0]
        #print('Infected w/ symptoms: %.4f' % (np.sum(n_symp)/3711))
        #print('Infected w/o symptoms: %.4f' % (np.sum(n_asymp)/3711))

        # Diamond Princess: 14 deaths (0.3776%) (JIID)
        #print('Deaths: 14 (JIID), %.4f%%' % (14/self.NP*100))


    def createBN(self):
        bn = gum.fastBN('Age{0-9|10-19|20-29|30-39|40-49|50-59|60-69|70-79|80-89|90-99}->PofS{not susceptible|susceptible};' +
                'Gender{male|female}->PofS;' +
                'PofS->COVID-19 Status{Infected, w/ Symptoms|Infected, w/o Symptoms|Not Infected};' +
                'COVID-19 Status->Tested Positive{no|yes};' +
                'FNR{1%|2%|3%|4%|5%|6%|7%|8%|9%|10%|11%|12%|13%|14%|15%}->Tested Positive;' +
                'FPR{0.25%|0.50%|0.75%|1.00%|1.25%|1.50%|1.75%|2.00%|2.25%|2.50%|2.75%|3.00%}->Tested Positive;' +
                'IPR{<=13%|14%|15%|16%|17%|18%|19%|20%|21%|22%|23%|24%|>=25%}->Tested Positive;' +
                'IPR->COVID-19 Status;' +
                'COVID-19 Status->IFR{0.0%|0.1%|0.2%|0.3%|0.4%|0.5%|0.6%|0.7%|0.8%|0.9%|1.0%}')

        #gnb.showBN(bn, size='9')
        bn.cpt('Age').fillWith(1).normalize()
        bn.cpt('Gender').fillWith(1).normalize()
        bn.cpt('PofS').fillWith(1).normalize()
        bn.cpt('FNR').fillWith(1).normalize()
        bn.cpt('FPR').fillWith(1).normalize()
        bn.cpt('IPR').fillWith(1).normalize()
        bn.cpt('COVID-19 Status').fillWith(1).normalize()
        bn.cpt('IFR').fillWith(1).normalize()

        return bn


    def populatingCPTs(self, bn) -> None:
        ## male, female
        bn.cpt('Gender')[:] = [0.55, 0.45]

        # median age (Moryarti, 2020): 
        #    crew: 36yo (IQR 29-43) 
        #    passenger: 69yo (IQR 62-73)
        # considering age [0-50 51-100]
        # stratified data from JIID's report, 2020
        total_age = [16, 23, 347, 428, 334, 398, 923, 1015, 216, 11]
        bn.cpt('Age')[:] = np.divide(total_age, self.NP)

        # false negative rates of between 2% and 29% (equating to sensitivity of 71-98%)
        # FPR: 0.25% interval, peak at 1.68%
        # 12 states: 0.25%|0.50%|0.75%|1.00%|1.25%|1.50%|1.75%|2.00%|2.25%|2.50%|2.75%|3.00%
        FPR_v,_ = self.tnorm_dist(mean=0.5, std_dev=np.sqrt(0.0168 / 2), bins=12)
        bn.cpt('FPR')[:] = FPR_v / np.sum(FPR_v)

        # FNR: 1% interval, peak at 10.12%
        # 15 states: 1%|2%|3%|4%|5%|6%|7%|8%|9%|10%|11%|12%|13%|14%|15%
        FNR_v,_ = self.tnorm_dist(mean=0.65, std_dev=np.sqrt(0.1012 / 10), bins=15)
        bn.cpt('FNR')[:] = FNR_v / np.sum(FNR_v)

        #print('FPR: ', bn.cpt('FPR')[:])
        #print('FNR: ', bn.cpt('FNR')[:])

        # How "susceptible" a person is based on "age":
        # Age{0-9|10-19|20-29|30-39|40-49|50-59|60-69|70-79|80-89|90-99}
        age_w = [(x+1.2) * 1 for x in range(1,11)]

        # PofS
        for gender in {0,1}:
            gender_w = 0.4 if gender == 0 else 0.2
            for i,age_prop in enumerate(bn.cpt('Age').tolist()):
                # weight for each age interval
                pofs_sus = age_w[i] * gender_w * age_prop
                # sometimes pofs_sus is higher than 1, so 1-pofs_sus will be negative
                pofs_sus = pofs_sus if pofs_sus <= 1 else 1
                # normalize to avoid get out of bounds
                pofs = [1-pofs_sus, pofs_sus]
                pofs = pofs / np.sum(pofs)
                bn.cpt('PofS')[{'Gender':gender, 'Age':i}] = pofs        

        # IPR: for Diamond Princess is around 19.18%
        # 13 states:  <=13%|14%|15%|16%|17%|18%|19%|20%|21%|22%|23%|24%|>=25%
        IPR_v,_ = self.tnorm_dist(mean=0.5, std_dev=np.sqrt(0.1012 / 10), bins=13)
        bn.cpt('IPR')[:] = IPR_v / np.sum(IPR_v)
        #plt.plot(np.arange(13,26), IPR_v, 'r-o');

        # COVID-19 Status
        # Inf. w/ Symp.: 0; Inf. w/o Symp.: 1; Not Inf.: 2
        # parents: IPR, PofS
        bn.cpt('COVID-19 Status')[{'IPR':2, 'PofS':0}] = [0.02, 0.02, 0.94]
        bn.cpt('COVID-19 Status')[{'IPR':2, 'PofS':1}] = [0.04, 0.05, 0.91]
        bn.cpt('COVID-19 Status')[{'IPR':6, 'PofS':0}] = [0.04, 0.05, 0.91]
        bn.cpt('COVID-19 Status')[{'IPR':6, 'PofS':1}] = [0.09, 0.10, 0.81]
        bn.cpt('COVID-19 Status')[{'IPR':10, 'PofS':0}] = [0.17, 0.12, 0.71]
        bn.cpt('COVID-19 Status')[{'IPR':10, 'PofS':1}] = [0.27, 0.12, 0.61]


        # 'Tested Positive' (2 states) depends on:
        #    - COVID-19 Status: 3 states
        #    - FNR: 15 states
        #    - FPR: 12 states
        #    - IPR: 13 states
        # Fenton's paper: (IPR*(1-FNR)) + ((1-IPR)*FPR)
        # Fenton's book "Boolean node" p. 253
        for i in range(3): # COVID-19 Status
            for j in range(15): # FNR
                for k in range(12): # FPR
                    for l in range(13): # IPR
                        # Error Rates
                        if (i == 0 or i == 1): # infected with and without symp.
                            er = bn.cpt('FNR')[j]
                        else:
                            er = bn.cpt('FPR')[k]
                            
                        # calculation based on COVID-19 status
                        covs_w = 0.98 if (i == 0 or i == 1) else 0.02
                        covs = covs_w * gum.getPosterior(bn, {}, 'COVID-19 Status')[i]

                        # Infection Prevalence Rate
                        ipr = bn.cpt('IPR')[l]

                        # weighted average (Fenton p.)
                        w = [1, 3, 2] # weights
                        w = w / np.sum(w) # normalizing
                        tpos_yes = (w[0]*er) + (w[1]*covs) + (w[2]*ipr)

                        bn.cpt('Tested Positive')[{'COVID-19 Status':i,
                                                'FNR':j,
                                                'FPR':k,
                                                'IPR':l}] = [1-tpos_yes, tpos_yes]
        bn.cpt('Tested Positive').normalizeAsCPT()

        # Diamond Princess: 14 deaths (0.3776%) (JIID)
        # IFR: 0.1% | 0.2% | 0.3% | 0.4% | 0.5% | 0.6% | 0.7%

        # Infected w/ Symp
        ifr_tmp,_ = self.tnorm_dist(mean=0.43, std_dev=np.sqrt(0.03), bins=11)
        ifr = ifr_tmp / np.sum(ifr_tmp)
        bn.cpt('IFR')[{'COVID-19 Status': 0}] = ifr

        # Infected w/o Symp.
        ifr_tmp,_ = self.tnorm_dist(mean=0.41, std_dev=np.sqrt(0.03), bins=11)
        ifr = ifr_tmp / np.sum(ifr_tmp)
        bn.cpt('IFR')[{'COVID-19 Status': 1}] = ifr

        # Not Infected
        ifr_tmp,_ = self.tnorm_dist(mean=0.35, std_dev=np.sqrt(0.01), bins=11)
        ifr = ifr_tmp / np.sum(ifr_tmp)
        bn.cpt('IFR')[{'COVID-19 Status': 2}] = ifr


    def doInference(self, bn, var_obs, evs={}):
        """Do inference on the Bayesian network based on the evidence set.
        This function will return the data regarding the variable observed as NumPy array.

        Parameters
        ----------
        bn : [type]
            Bayesian network.
        evs : dict
            evidence to be set according to PyAgrum format
        var_obs : list
            variable observed. The variable specified will be returned by the function.
        """

        # TODO: maybe add other inference methods?
        ie = gum.LazyPropagation(bn)

        ie.setEvidence(evs)
        ie.makeInference()

        # TODO: what if more than one var_obs????
        all_vars = {}
        for v in var_obs:
            all_vars[v] = ie.posterior(v).toarray()

        return all_vars

    def getBN(self):
        return self.bn