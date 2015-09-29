import random
import pitchhelpers as pth
from motif import *
import probabilityhelpers as ph
import rhythms as rhy
import scale as sc

#generating a motif beats long
def genMotif(beats):
    durations = rhy.randomDuration(beats)
    tot_durs = [sum(durations[:i]) for i in range(0, len(durations))]
    pitches = [random.choice([0,0,2,2,4,4,1,-1,-2])]
    for i in range(1, len(durations)):
        if tot_durs[i] == 2.0:
            probOnBeat = {-4: 1, -2:4, 0: 2, 2:4, 4:1} #try to make the on beat a member of the major triad
            probOnBeat = dict([(k,v) for k,v in probOnBeat.items() if abs(pitches[-1] - k) <= 4])
            if len(probOnBeat) == 0:
                probOnBeat = {pitches[-1] - 1:1, pitches[-1] + 1:1}
            pitches.append(pitches[0] + ph.probDictToChoice(probOnBeat))
        else:            
            #if pitches are too high/low, move towards the center
            if pitches[-1] > 12: 
                pitches.append(pitches[-1] - ph.probDictToChoice(sc.horizontalmarkov))
            elif pitches[-1] < 0:
                pitches.append(pitches[-1] + ph.probDictToChoice(sc.horizontalmarkov))
            #otherwise, move either up or down
            else:
                pitches.append(pitches[-1] + ph.probDictToChoice(sc.horizontalmarkov) * random.choice([1,-1]))
    return Motif(pitches, durations)

#altering a given motif
def alterMotif(motif, p_alter_pitch = 0.2, p_alter_rhythm = 0.2):
    new_durs = []
    new_pitches = []
    for i in range(0, len(motif.l1d)):
        beat = motif.l1d[i]
        beat_pitches = motif.l1p[i]
        ran1 = random.uniform(0,1) #used to determine rhythm changes
        ran2 = random.uniform(0,1) #used to determine pitch changes
        tmp_dur = []
        if beat == [1.0]: #either keep as quarter note, or transform to eighths or sixteenths
            if ran1 < p_alter_rhythm/2:
                tmp_dur = [0.25,0.25,0.25,0.25]
                tmp_pitches = [beat_pitches[0]]
                for i in range(0,3):
                    tmp_pitches.append(tmp_pitches[-1] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1]))
            elif ran1 < p_alter_rhythm:
                tmp_dur = [0.5,0.5]
                if ran2 < p_alter_pitch:
                    tmp_pitches = [beat_pitches[0] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1])]
                    tmp_pitches.append(tmp_pitches[-1] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1]))
                else:
                    tmp_pitches = [beat_pitches[0], beat_pitches[0] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1])]
            else:
                tmp_dur = [1.0]
                if ran2 < p_alter_pitch:
                    tmp_pitches = [beat_pitches[0] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1])]
                else:
                    tmp_pitches = beat_pitches
        elif beat == [0.5,0.5]: #either keep as eighths, or transform to sixteenths or quarter
            if ran1 < p_alter_rhythm/2:
                tmp_dur = [0.25,0.25,0.25,0.25]
                if ran2 < p_alter_pitch:
                    tmp_pitches = [beat_pitches[0] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1])]
                    for i in range(0,3):
                        tmp_pitches.append(tmp_pitches[-1] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1]))
                else:
                    tmp_pitches = [beat_pitches[0], beat_pitches[0] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1]), beat_pitches[1], beat_pitches[1] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1])]
            elif ran1 < p_alter_rhythm:
                tmp_dur = [1.0]
                if ran2 < p_alter_pitch:
                    tmp_pitches = [beat_pitches[0] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1])]
                else:
                    tmp_pitches = [beat_pitches[0]]
            else:
                tmp_dur = [0.5,0.5]
                if ran2 < p_alter_pitch:
                    tmp_pitches = [beat_pitches[0] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1]), beat_pitches[1]]
                else:
                    tmp_pitches = beat_pitches
        elif beat == [0.25,0.25,0.25,0.25]: #either keep as sixteenths, or transform to eighths or quarter
            if ran1 < p_alter_rhythm/2:
                tmp_dur = [0.5,0.5]
                if ran2 < p_alter_pitch:
                    tmp_pitches = [beat_pitches[0] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1])]
                    tmp_pitches.append(tmp_pitches[-1]  + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1]))
                else:
                    tmp_pitches = [beat_pitches[0], beat_pitches[2]]
            elif ran1 < p_alter_rhythm:
                tmp_dur = [1.0]
                if ran2 < p_alter_pitch:
                    tmp_pitches = [beat_pitches[0] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1])]
                else:
                    tmp_pitches = [beat_pitches[0]]
            else:
                tmp_dur = [0.25,0.25,0.25,0.25]
                if ran2 < p_alter_pitch:
                    tmp_pitches = [beat_pitches[0] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1])]
                    for i in range(0,3):
                        tmp_pitches.append(tmp_pitches[-1] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1]))
                else:
                    tmp_pitches = beat_pitches
        else: #if the beat is neither all eighth notes nor sixteenth notes nor a quarter, keep the rhythm constant
            tmp_dur = beat
            tmp_pitches = []
            for pitch in beat_pitches:
                ran2 = random.uniform(0,1)
                if ran2 < p_alter_pitch:
                    tmp_pitches.append(pitch + ph.probDictToChoice(sc.horizontalmarkov))
                else:
                    tmp_pitches.append(pitch)
        new_durs.extend(tmp_dur)
        new_pitches.extend(tmp_pitches)
    return Motif(new_pitches, new_durs)
                
#transform motif to an ending          
def transformToEnding(motif, cord = [0,2,4], cord2 = [4,6,8], true_end = False):
    if type(motif) is list:     #because of a bug which was causing motif to be wrapped in a list itself
        motif = motif[0]
    #keep the same first half
    first_half_durs = []
    first_half_pitches = []
    first_half_durs.extend(motif.l1d[0])
    first_half_pitches.extend(motif.l1p[0])
    if sum(first_half_durs) < 2.0:
        first_half_durs.extend(motif.l1d[1])
        first_half_pitches.extend(motif.l1p[1])
    if true_end: #if this is the end of a major movement, need a half note of the tonic 
        first_half_durs.append(2.0)
        first_half_pitches.append(pth.getClosestPCDegree(first_half_pitches[-1], 0))
        return Motif(first_half_pitches, first_half_durs)
    else:
        what_end = random.uniform(0,1)
        #end with either a quarter note quarter rest, quarter note eighth rest eighth note, or half note
        if what_end < 0.3:
            first_half_durs.extend([1.0,-1.0])
            first_half_pitches.extend([sc.closestNoteDegreeInChord(first_half_pitches[-1], cord), -1])
            #rest, beat
        elif what_end < 0.7:
            #quarternote, eight rest, eighth note
            first_half_durs.extend([1.0,-0.5, 0.5])
            first_half_pitches.extend([sc.closestNoteDegreeInChord(first_half_pitches[-1], cord), -1, sc.closestNoteDegreeInChord(first_half_pitches[-1], cord2)])
        else:
            #half note
            first_half_durs.extend([2.0])
            first_half_pitches.append(sc.closestNoteDegreeInChord(first_half_pitches[-1], cord))
    return Motif(first_half_pitches, first_half_durs)