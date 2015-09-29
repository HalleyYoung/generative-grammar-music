# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 14:55:55 2014

@author: halley
"""
from noteconstants import *
import music21helpers as mh
from music21 import *
import probabilityhelpers as ph
import melodyhelpers as mlh
"""
rules can be chords - schenkerian analysis in terms of l system

make each rule 2-beats
make each rule have a certain chance of changing

"""
rule_probs = {}
rule_probs["A"] = {0:0.3, 1:0.35, 2:0.35}
rule_probs["B"] = {0:0.4, 1:0.3, 2:0.3}
rule_probs["C"] = {0:0.4, 1:0.3, 2:0.3}
rule_probs["D"] = {0:0.4, 1:0.3, 2:0.3}
rule_probs["E"] = {0:0.4, 1:0.3, 2:0.3}
rule_probs["F"] = {0:0.4, 1:0.3, 2:0.3}
rule_probs["Gs"] = {0:0.5, 1:0.5}

rules = {}
rules["A"] = [["A-2", "C-2", "D-2", "E-2", "B-2", "Gs-2", "A-4"], ["E-8", "Gs-4", "A-4"], ["A-6", "B-2", "C-6", "A-2"]]
rules["B"] = [["B-4", "E-4", "C-4", "A-2", "B-2"],["E-4", "C-4", "D-2", "C-2", "B-4"], ["B-8", "A-2", "C-2", "B-4"]]
rules["C"] = [["C-8", "Gs-4", "A-4"], ["C-4", "E-4", "D-4", "C-4"], ["C-4", "D-4", "C-4", "A-4"]]
rules["D"] = [["D-6", "E-2", "A-4", "Gs-4"], ["D-2", "C-2", "B-4", "D-4", "D-4"], ["D-4", "E-4", "Gs-4", "A-4"]]
rules["E"] = [["E-4", "A-2", "C-2", "E-4", "E-4"],  ["A-8", "D-6", "E-2"], ["E-4", "Gs-2", "A-2", "B-2", "E-2", "E-4"]]
rules["F"] = [["F-4", "D-6", "C-2", "A-4"], ["F-8", "E-4", "F-4"], ["F-4", "D-4", "C-4", "E-4"]]
rules["Gs"] = [["Gs-4", "A-8", "B-4"],  ["Gs-2", "A-2", "Gs-2", "E-2", "Gs-8"]]

def genLSystem(iterations, start_array, rules):
    def getChoice(item, rules):
        return rules[item.split("-")[0]][ph.probDictToChoice(rule_probs[item.split("-")[0]])]
    if (iterations == 1):
        return start_array
    else:
        new_array = []
        for i in range(0, len(start_array)):
            item = start_array[i]
            if item[0] in rules:
                new_array.extend(genLSystem(iterations - 1, getChoice(item, rules), rules))
            else:
                new_array.append(item)
        return new_array     
        
def notesFromRuleOutput(routput):
    notes = []
    for i in range(0, len(routput)):
        new_note = note.Note()
        if i > 1:
            new_note.midi = mlh.getClosestPC(notes[-1].midi, midi_notes[routput[i].split('-')[0]])
        else:
            new_note.midi = midi_notes[routput[i].split('-')[0]] + 72
        new_note.quarterLength = int(routput[i][-1])/4.0
        notes.append(new_note)
    return notes
    
def fixNoteLens(notes):
    new_notes = []
    cur_rhythm = 0
    for note in notes:
        r = note.quarterLength
        if r + cur_rhythm == 4.0:
            cur_rhythm = 0
            new_notes.append(note)
        elif r + cur_rhythm > 4.0:
            note.quarterLength = 4.0 - cur_rhythm
            cur_rhythm = 0
            new_notes.append(note)
        else:
            new_notes.append(note)
            cur_rhythm += r
    return new_notes
    
start_array = ["A-8", "E-8", "Gs-8", "A-8"]
iterations = 4
g = genLSystem(iterations, start_array, rules)
notes = notesFromRuleOutput(g)
score = stream.Stream()
score.append(notes)
score.show('musicxml')