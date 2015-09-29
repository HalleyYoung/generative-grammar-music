# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 12:15:31 2014

@author: halley
"""

"""
fold function
f: the function to apply
l: the list to fold
a: the accumulator
"""
def fold(f, l, a):
    return a if len(l) == 0 else fold(f, l[1:], f(a, l[0]))


#return if small is sub_str of large
def is_substr(small, large):
    for l in range(0, len(large)):
        string = ""
        for e in range(l, len(large)):
            string.append(e)
            if string == small:
                return True
    return False

#concat list    
def concat(xss):
    return [j for i in xss for j in i]


#get item in array number n mod len(array)    
def getWrap(array, index):
    if index < len(array):
        return array[index]
    else:
        return array [index % len(array)]