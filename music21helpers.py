# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 07:47:21 2014

@author: halley
"""

from music21 import *
from constants import *
import scale as sc
import functionalhelpers as fh
import random
import pitchhelpers as pth

"""def motifsToPitchesDurs(motifs):
    durs = [i.l0d for i in motifs]
    #cat_durs = fh.concat(durs)
    pitches = [i.l0p for i in motifs]
    prev = pitches[0][0]
    #tot_durs = [sum(cat_durs[:i]) for i in range(0, len(cat_durs)) ]
    n = 0    
    
    for i in range(0, len(pitches)):
        if i > 0:
            prev = pitches[i - 1][-1]
            #print (prev)
        for j in range(1, len(pitches[i])):
            if abs(pitches[i][j] - prev) > 4:
                print("old " + str(pitches[i][j]) + " prev " + str(prev)) 
                pitches[i][j] = pth.getClosestPCDegree(prev, pitches[i][j])
                print("new " + str(pitches[i][j]) + "\n")
            prev = pitches[i][j]
        n += 1
    return (pitches, durs)"""
    
def motifsToPitchesDurs(motifs):
    pitches = [i.l0p for i in motifs]
    durs = [i.l0d for i in motifs]
    return (pitches, durs)
    new_pitches = [pitches[0]]
    for i in range(1, len(pitches)): 
        if type(pitches[i]) == tuple or type(new_pitches[-1]) == tuple:
            new_pitches.append(pitches[i])
        
    np = []
    n = 0
    for i in range(0, len(motifs)):
        np.append([])
        for j in range(0, len(motifs[i].l0p)):
            np[-1].append(new_pitches[n])
            n += 1
    return (np, durs)

def pitchesDursToPart(pitches, durs, key_area, octave = 5):
    durs = fh.concat(durs)
    midi_pitches = []    
    for i in range(0, len(pitches)):
        skale = scales["G major"] if key_area[i] == 7 else scales["C major"]
        for j in range(0, len(pitches[i])):
            if type(pitches[i][j]) == tuple:
                cord = tuple(sc.degreeToNote(pitch, octave, scale = skale) for pitch in pitches[i][j])
                midi_pitches.append(cord)
            else:
                midi_pitches.append(sc.degreeToNote(pitches[i][j], octave = octave, scale = skale))
                    
    #pitches, durs = smooth.smoothOut(pitches, durs, leading)
    score = listsToPart(midi_pitches, durs)
    return score

#convert list of motifs to part
def motifsToPart(motifs, key_area, leading = True, octave = 5):
    durs = fh.concat([i.l0d for i in motifs])
    pitches = [i.l0p for i in motifs]
    """
    prev = pitches[0][0]
    tot_durs = [sum(durs[:i]) for i in range(0, len(durs)) ]
    n = 0

    for i in range(0, len(pitches)):
        if i > 0:
            prev = pitches[i - 1][-1]
        for j in range(1, len(pitches[i])):
            if tot_durs[n] % 1.0 != 0:
                if pitches[i] == prev:
                    pitches[i] += random.choice([1,-1]) 
            if pitches[i][j] > 14:
                if abs(prev - pitches[i][j] - 7) < 4:
                    pitches[i][j] = pitches[i][j] - 7
            elif pitches[i][j] < 0:
                if abs(prev - pitches[i][j] + 7) < 4:
                    pitches[i][j] = pitches[i][j] + 7
            #elif abs(pitches[i][j] - prev) > 4:
            #    pitches[i][j] = pth.getClosestPCDegree(pitches[i][j - 1], pitches[i][j])
            prev = pitches[i][j]
        n += 1 
    """
    #if there is a stretch where too low or high, fix
    midi_pitches = []    
    for i in range(0, len(pitches)):
        if key_area[i] == 0:
            midi_pitches.extend(sc.degreesToNotes(pitches[i], scale = scales["C major"], octave = octave))
        elif key_area[i] == 7:
            new_pitches = sc.degreesToNotes(pitches[i], scale = scales["G major"], octave = octave)
            midi_pitches.extend(new_pitches)

    #pitches, durs = smooth.smoothOut(pitches, durs, leading)
    score = listsToPart(midi_pitches, durs)
    return score
    
#convert score object to a list of notes
def scoreToNotes(score, part):
    notes = [] 
    parts = score.parts
    prt = parts[part]
    for i in range(1, len(prt)):
        measure = prt[i]
        for note in measure.elements:
            if type(note) is note.Note or type(note) is note.Rest:
                notes.append(note)
    return notes

#get pitches from score
def scoreToPitches(score, part):
    notes = scoreToNotes(score, part)
    return map(lambda i: i.midi, notes)

#get durations from score
def scoreToDurations(score, part):
    notes = scoreToNotes(score, part)
    return map(lambda i: i.quarterLength, notes)

#convert score object to (pitches[], durations[])
def scoreToPitchesDurations(score, part):
    notes = scoreToNotes(score, part)
    return (map(lambda i: i.midi, notes), map(lambda i: i.quarterLength, notes))

#convert list of notes to (pitches[], durations[])
def notesToPitchesDurations(notes):
    pitches = map (lambda i: i.midi, notes)
    durations = map(lambda i: i.quarterLength, notes)
    return (pitches, durations)

#from tuple of midi+pitch, duration to note
def tupleToNote(midi_pitch_and_duration):
    midi_pitch, duration = midi_pitch_and_duration
    if midi_pitch > 0 and duration > 0:
        n = note.Note()
        n.midi = midi_pitch
        n.quarterLength = duration
        return n
    else: 
        n = note.Rest()
        n.quarterLength = abs(duration)
        return n

#convert part object to list of measure objects    
def partToMeasures(part):
    measures = []
    for measure in part[1:]:
        measures.append(measure)
    return measures
    
#two lists of pitch/duration to list of notes
def listsToNotes(pitches, durations):
    notes = []
    for i in range(0, min(len(durations), len(pitches))):
        if type(pitches[i]) == tuple:
            n = chord.Chord(pitches[i])
            n.quarterLength = durations[i]
            notes.append(n)
        elif durations[i] < 0:
            n = note.Rest()
            n.isRest = True
            n.quarterLength = abs(durations[i])
            notes.append(n)
        else:
            notes.append( tupleToNote((pitches[i], durations[i])) )
    return notes

#returns a list of keysignatures for a given part
def partToKeySignatures(part):
    keys = []
    measures = partToMeasures(part)
    keysigs = map(lambda i: i.keySignature, measures)
    for keysig in keysigs:
        if keysig is not None:
            keys.append(keysig)
    return keys
    
#list of tuples to list of notes
def tuplesToNotes(pitches_and_durations):
    return map(tupleToNote, pitches_and_durations)

#list of notes to stream of notes    
def notesToStream(lst):
    s = stream.Stream()
    for l in lst:
        s.append(l)
    return s

#returns a part from a list of notes
def notesToPart(lst):
    s = stream.Part()
    for l in lst:
        s.append(l)
    return s
    
#tuples to stream
def tuplesToStream(pitches_and_durations):
    return notesToStream(tuplesToNotes(pitches_and_durations))
    
#lists to stream        
def listsToStream(pitches, durations):
    return notesToStream(listsToNotes(pitches, durations))    

#lists of midi pitches and durations to a part object
def listsToPart(pitches, durations):
    return notesToPart(listsToNotes(pitches, durations))

#lists of scale degrees and durations to a stream object
def listsDegreesToStream(degrees, durations, octave = 5, scale = scales["major"]):
    pitches = sc.degreesToNotes(degrees, octave, scale)
    return listsToStream(pitches, durations)

#lists of scale degrees and durations to a part object
def listsDegreesToPart(degrees, durations, octave = 5, scale = scales["major"]):
    pitches = sc.degreesToNotes(degrees, octave, scale)
    return listsToPart(pitches, durations)

#takes f :: pitch -> pitch and notes, returns notes
def mapPitchesOnNotes(f, notes):
    pitches, durations = notesToPitchesDurations(notes)
    return listsToNotes(f(pitches), durations)
    
#takes f :: duration -> duration and notes, returns notes
def mapDurationsOnNotes(f, notes):
    pitches, durations = notesToPitchesDurations(notes)
    return listsToNotes(pitches, f(durations))

#show the given pitches and durations combination in musicxml format
def showLists(pitches, durs):
    score = listsToStream(pitches, durs)
    score.show('musicxml')

#show the given scale degrees and durations combination in musicxml format
def showDegreesDurs(degrees, durs):
    pitches = sc.degreesToNotes(degrees)
    score = listsToStream(pitches, durs)
    score.show('musicxml')    
    
#show the given list of motifs in musicxml format
def showPhrase(motifs, degrees = True):
    pitches = []
    mpitches = ([i.l0p for i in motifs])
    for i in range(0, len(mpitches)):
        pitches.extend(mpitches[i][:len(motifs[i].l0d)])
    if degrees:
        pitches = sc.degreesToNotes(pitches)
    durs = fh.concat([i.l0d for i in motifs])
    score = listsToStream(pitches, durs)
    score.show('musicxml')

def writePhrase(motifs,  fname, degrees = True):
    pitches = []
    mpitches = ([i.l0p for i in motifs])
    for i in range(0, len(mpitches)):
        pitches.extend(mpitches[i][:len(motifs[i].l0d)])
    if degrees:
        pitches = sc.degreesToNotes(pitches)
    durs = fh.concat([i.l0d for i in motifs])
    score = listsToStream(pitches, durs)
    score.write(fmt = 'musicxml', fp = fname)