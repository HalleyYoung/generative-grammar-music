# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 07:56:14 2014

@author: halley
"""
import random
from functionalhelpers import *
from numpy import product
import operator

#return random uniform
def getUniform():
    return random.uniform(0,1)

#from dict of probabilities to a choice based on the probabilities
def probDictToChoice(pdict):
    renormalizeProbs(pdict)
    ps = {}
    prev = 0
    for (k,v) in pdict.items():
        #print(k)
        ps[k] = prev  + v
        prev = ps[k]
    r = random.uniform(0.0, 1.0)
    psitems = sorted(ps.items(), key = operator.itemgetter(1))
    for k,v in psitems:
        #print("k " + k)
        if r <= v:
            return k
    return ps.keys()[-1]

#given dict of (k, p(k)), renormalize so sum of all p(k) == 1
def renormalizeProbs(probdict):
    sumps = sum(probdict.values())
    for k in probdict.keys():
        probdict[k] = (probdict[k] + 0.0) / sumps

        
#return last number in a string represenation of a list of numbers
def lastNum(numstr):
    nums = [float(i) for i in numstr.split(' ')]
    return nums[-1]

#return first number in a string represenation of a list of numbers
def firstNum(numstr):
    nums = [float(i) for i in numstr.split(' ')]
    return nums[0]
        
#geometric mean
def geometricMean(probs):
    return product(probs) ** (1.0/len(probs))
    
#get the geometric mean of each dict key among a list of probability dicts
def geometricMeanPDicts(pdicts):
    new_pdict = {}
    #first, get all values
    all_keys = list(set(concat(map(lambda i: i.keys(), pdicts))))
    for key in all_keys:
        probs = []
        for pdict in pdicts:
            if key in pdict:
                probs.append(pdict[key])
            else:
                probs.append(0)
        new_pdict[key] = geometricMean(probs)
    return new_pdict