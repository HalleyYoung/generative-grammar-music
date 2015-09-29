from noteconstants import *
import music21helpers as mh
import functionalhelpers as fh
import rhythms as rh
from music21 import *
import random

rules = {}
letters = "ABCDEFG"
ends = {}
ends["A"] = ["A", "E"]
for i in range(1,len(letters)):
    letter = letters[i]
    begends[letter] = [letter]
    begends[letter].append(fh.getWrap(letters, random.choice([i + 2, i + 4, i + random.randint(1,6)])))
    
rules = {}    
for letter in letters:
    for end in ends:
        newrhythm = rh.randomThree()
        
        #get walk in x steps from a to b, no more than 5 steps per