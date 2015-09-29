# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 11:48:37 2014

@author: halley
"""
import probabilityhelpers as ph
from functionalhelpers import *
import random

#These two functions are used to convert between string and list representations of rhythms (because lists aren't hashable and therefore can't be used in the probability dict)
def strNum(rhys):
    return ' '.join([str(i) for i in rhys])
def strToRhy(r_str):
    return [float(i) for i in r_str.split(' ')]
    
#set probabilities for one beat
onerhys = [[1.0], [0.5,0.5], [0.25,0.25,0.25,0.25]]#, #[0.5,0.25,0.25], [0.25,0.25,0.5]]
oneprobs = {}
oneprobs["1.0"] = 0.35
oneprobs["0.5 0.5"] = 0.4
oneprobs["0.25 0.25 0.25 0.25"] = 0.05
oneprobs["0.5 0.25 0.25"] = 0.01
ph.renormalizeProbs(oneprobs)

#set probabilities for two beats
tworhys = []
twoprobs = {}
for i in range(0, len(onerhys)):
    tworhys.append([onerhys[i], onerhys[i]])
    for j in range(i + 1, len(onerhys)):
        tworhys.append([onerhys[i], onerhys[j]])
        tworhys.append([onerhys[j], onerhys[i]])
for rhys in tworhys:
    rhystr = ' '.join(map(strNum, rhys))
    probs = map(lambda i: oneprobs[strNum(i)], rhys)
    twoprobs[rhystr] = ph.geometricMean(probs)
    if (rhys[0][0] == rhys[1][0]):
        twoprobs[rhystr] *= 4
    elif (rhys[0][0] > rhys[1][0]):
        twoprobs[rhystr] *= 2
twoprobs['1.5 0.5'] = 0.3
twoprobs['2.0'] = 0.2
twoprobs['1.5 0.25 0.25'] = 0.2 
twoprobs['0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25'] = 0.2   
ph.renormalizeProbs(twoprobs)

#set probabilities for four beats
twos = twoprobs.keys()
fourrhys = []
for i in range(0, len(twos)):
    fourrhys.append([twos[i], twos[i]])
    for j in range(i, len(twos)):
        fourrhys.append([twos[i], twos[j]])
        fourrhys.append([twos[j], twos[i]])

fourprobs = {}
for rhys in fourrhys:
    rhylist = map(strToRhy, rhys)
    prob = ph.geometricMean(map(lambda i: twoprobs[i], rhys))
    if rhylist[0] == rhylist[1]:
        prob *= 6
    elif rhylist[0][0] == rhylist[1][0]:
        prob *= 3
    fourprobs[' '.join(rhys)] = prob
fourprobs['3.0 0.5 0.5'] = 0.05
fourprobs['3.0 1.0'] = 0.05
ph.renormalizeProbs(fourprobs)

#return a random one beat rhythm
def randomOneProb():
    return strToRhy(ph.probDictToChoice(oneprobs))

#return a random two beat rhythm
def randomTwoProb():
    return strToRhy(ph.probDictToChoice(twoprobs))

#return a random three beat rhythm
def randomThreeProb():
    two = strToRhy(ph.probDictToChoice(twoprobs))
    two.extend(strToRhy(ph.probDictToChoice(oneprobs)))
    return two
    
#return a random four beat rhythm
def randomMeasure():
    return strToRhy(ph.probDictToChoice(fourprobs))
    
#return a random rhythm of duration dur
def randomDuration(dur):
    if dur == 1:
        return randomOneProb()
    elif dur == 2:
        return randomTwoProb()
    elif dur == 3:
        return randomThreeProb()
    elif dur == 4:
        return randomMeasure()
    elif dur == 6:
        rand_dur = []
        rand_dur.extend(randomMeasure())
        rand_dur.extend(randomTwoProb())
        return rand_dur
    elif dur == 8:
        rand_dur = []
        rand_dur.extend(randomMeasure())
        rand_dur.extend(randomMeasure())
        return rand_dur
        
#return a similar rhythm to the previous rhythm
def alterRhythm(durs, p_alter):
    new_durs = []
    n = 0 #dur index
    while (n < len(durs)):
        durs_appended = False
        ran_alter = ph.getUniform() #random seed
        if (n < len(durs) - 4):
            if (durs[n] == 0.25 and durs[n+1] == 0.25 and durs[n+2] == 0.25 and durs[n+3] == 0.25):
                if ran_alter < p_alter / 2:
                    new_durs.append(1)
                elif ran_alter < p_alter:
                    new_durs.extend([0.5,0.5])
                else:
                    new_durs.extend([0.25,0.25,0.25,0.25]) #keep it the same
                durs_appended = True
                n += 4
        if (n < len(durs) - 2):
            if (durs[n] == 0.5 and durs[n+1] == 0.5):
                if ran_alter < p_alter / 2:
                    new_durs.append(1)
                elif ran_alter < p_alter:
                    new_durs.extend([0.25,0.25,0.25,0.25])
                else:
                    new_durs.extend([0.5, 0.5]) #keep it the same
                durs_appended = True
                n += 2
        if durs[n] == 1.0:
            if ran_alter < p_alter / 2:
                new_durs.extend([0.5,0.5])
            elif ran_alter < p_alter:
                new_durs.extend([0.25,0.25,0.25,0.25])
            else:
                new_durs.append(1.0)
            durs_appended = True
            n += 1
        if not durs_appended:
            new_durs.append(durs[n])
            n += 1
    #print(sum(new_durs) == sum(durs))
    return new_durs

prob_dict = {'0.5 0.25 0.25':0.05, '0.25 0.25 0.5': 0.05, '1.0': 0.1, '0.5 0.5': 0.2, '0.25 0.25 0.25 0.25':0.15}
two_prob_dict = {}
prob_dict_keys = prob_dict.keys()
for i in range(0, len(prob_dict_keys)):
    two_prob_dict[prob_dict_keys[i] + ' ' + prob_dict_keys[i]] = 1.2*prob_dict[prob_dict_keys[i]]
    for j in range(i + 1, len(prob_dict_keys)):
        two_prob_dict[prob_dict_keys[i] + ' ' + prob_dict_keys[j]] = ph.geometricMean([prob_dict[prob_dict_keys[i]], prob_dict[prob_dict_keys[j]]])
        two_prob_dict[prob_dict_keys[j] + ' ' + prob_dict_keys[i]] = ph.geometricMean([prob_dict[prob_dict_keys[i]], prob_dict[prob_dict_keys[j]]])        
two_prob_dict['1.5 0.5'] = 0.05
two_prob_dict['1.5 0.25 0.25'] = 0.02

def randomHalfRhythm(short = False):
    if short:
        return random.choice([[1.5, 0.5], [1.5, 0.25, 0.25], [1.0, 1.0], [1.0,0.5,0.5], [0.5,0.5,1.0]])
    else:        
        return strToRhy(ph.probDictToChoice(two_prob_dict))
        
def halfRhythmDict():
    return two_prob_dict

def randomHalfQuarterEighths():
    half_prob_dict = {'1.0 0.5 0.5':0.3, '00.5 0.5 1': 0.1, '0.5 0.5 0.5 0.5':0.25, '1.0 1.0': 0.15}
    return strToRhy(ph.probDictToChoice(half_prob_dict))