# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 10:44:14 2014

@author: halley
"""

import random
import probabilityhelpers as ph
import scale as sc

horizontalmarkov = {1:20, 2:8, 3:2, 4:1}

#change size of intervals
def changeIntervals(pitches, direc=1):
    intervals = map(lambda i: pitches[i] - pitches[i - 1], range(1, len(pitches)))
    new_intervals = []
    for interval in intervals:
        if interval < 0:
            new_intervals.append(interval + random.randint(0, 2) * direc)
        else:
            new_intervals.append(interval + random.randint(0, 2) * direc * -1)
    new_pitches = [pitches[0]]
    for i in range(0, len(intervals)):
        new_pitches.append(new_pitches[i] + intervals[i])
    return new_pitches

def numberInDirection(notes):
    intervals = [notes[i] - notes[i - 1] for i in range(1, len(notes))]
    for i in range(1, len(intervals)):
        if (intervals[i] > 0) != (intervals[i - 1] > 0):
            return i
    return len(intervals)

def randomNextDegree(prev_note = 0):    
    interval = ph.probDictToChoice(sc.horizontalmarkov) * random.choice([-1,1])
    return prev_note + interval

def getClosestPCDegree(p1, p2):
    above = ((p1/7) + 1)*7 + (p2%7)
    mid = ((p1/7)*7) + (p2%7)
    below = ((p1/7) - 1) * 7 + (p2 % 7)
    if abs(p1 - above) < min(abs(p1 - below), abs(p1 - mid)):
        return above
    elif abs(p1 - mid) < min(abs(p1 - below), abs(p1 - above)):
        return mid
    else:
        return below

def getClosestPCDegrees(p1, p_next):
    all_notes = [getClosestPCDegree(p1, p_next[0])]
    for note in p_next[1:]:
        all_notes.append(getClosestPCDegree(all_notes[-1], note))            
    return all_notes
    
def getClosestPC(p1, p2):
    above = ((p1/12) + 1)*12 + (p2%12)
    mid = ((p1/12)*12) + (p2%12)
    below = ((p1/12) - 1) * 12 + (p2 % 12)
    if above > 84:
        return mid
    if below < 48:
        return mid
    else:
        if abs(p1 - above) < max(abs(p1 - below), abs(p1 - mid)):
            return above
        elif abs(p1 - mid) < max(abs(p1 - below), abs(p1 - above)):
            return mid
        else:
            return below


  
def randomWalkBeginningEndDegrees(start, end, n, any_octave = False):
    if n == 1:
        return [start]
    elif n == 2:
        return [start, end]
    elif n == 3:
        return [start, random.choice([start - 1] + range(start + 1, end) + [end + 1]), end]
    else:
        while (True):
            degs = [start]
            for i in range(1, n - 2):
                if degs[-1] < 0:
                    degs.append(degs[-1] + ph.probDictToChoice(sc.horizontalmarkov))
                elif degs[-1] > 14:
                    degs.append(degs[-1] + ph.probDictToChoice(sc.horizontalmarkov)*-1)
                else:
                    degs.append(degs[-1] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,-1,-1,1]))
            if any_octave:
                end = getClosestPCDegree(degs[-1], end)
            if end == degs[-1]:
                second_to_last = random.choice([end - 2, end - 1, end + 1, end + 2])
            else:
                second_to_last = random.randint(degs[-1] + 1, end) if end > degs[-1] else random.randint(end + 1, degs[-1])
            degs.append(second_to_last)
            degs.append(end)
            if abs(degs[-1] - degs[-2]) < 3:
                break
        return degs
    """    
    if any_octave:
        end = getClosestPC(start, end)
    if n == 2:
        return [start, end]
    elif n == 3:
        return [start, start + random.choice([(start + end)/2 - 2, (start + end)/2 + 2]), end]
    elif n == 4:
        return [start, start + random.choice([(start + end)/2 - 2, (start + end)/2 + 2]), start + random.choice([(start + end)/2 - 1, (start + end)/2 + 1]), end]
    else:
        start_template = randomWalkBeginningEndDegrees(start, end, 4, any_octave)
        for i in range(0, n - 4):
            where_to_insert = random.randint(0, i + 2)
            if start_template[where_to_insert + 1] > start_template[where_to_insert]:
                start_template.insert(where_to_insert, random.randint(start_template[where_to_insert] - 1, start_template[where_to_insert + 1] + 1))
            else:
                start_template.insert(where_to_insert, random.randint(start_template[where_to_insert + 1] - 1, start_template[where_to_insert] + 1))
        return start_template
     """  
        
#return pitches moving in opposite direction   
def oppositeDirection(pitches):
    how_much_changed = random.randint(2,3)
    new_pitches = pitches[:-how_much_changed]
    new_intervals = [pitches[i] - pitches[i - 1] for i in range(len(pitches) - how_much_changed, len(pitches))]
    for interval in new_intervals:
        new_pitches.append(new_pitches[-1] - interval)
    return new_pitches