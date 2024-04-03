# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 01:55:03 2024

@author: Thomas
"""

from Node import *
import math

def task5(msg):
    contents = msg.upper()
    # Construct dictionary to store frequency
    Text = "ETAONS"
    FreqCount = {l: 0 for l in Text}  # Initialize FreqCount dictionary
        
    # start counting
    for char in contents:
        if char in Text:
            FreqCount[char] += 1

    # Rearannge the letters
    SortedStr = ""
    while len(FreqCount) != 0:
        CurrentMaxCount = max(FreqCount.values())
            
        # Get all letters that may have the same count
        MaxLetters = []
        for key, val in FreqCount.items():
            if val == CurrentMaxCount:
                MaxLetters.append(key)
        
        # Get smallest letter
        Letter = min(MaxLetters)
        SortedStr += Letter
            
        FreqCount.pop(Letter)

        # Get wrong places counted
    MisplaceCount = 0
    if len(Text) != len(SortedStr):
        print("Wrong Inputs")
            
        return 0
        
    else:
        for charText,charSorted in zip(Text,SortedStr):
            if charSorted != charText:
                MisplaceCount += 1 
            
        # Calculate heuristic
        Heuristic = math.ceil(MisplaceCount/2)
        return Heuristic
    
def Greedy(aTree):
    Fringe = [aTree.ReturnRoot()]
    Expanded = []
    
    FringeSize = 1
    ExpandedSize = 0
    
    Node = Fringe.pop(0)
    
    while task5(Node.mState) != 0:
        break
        
    
    
    pass
    
def task6(algorithm, message_filename, dictionary_filename, threshold, letters, debug):
    Tree = CTree()
    
    Letters = list(letters)
    Letters.sort()
    swaps = []
    # Generate all swap patterns
    for i in range(len(Letters)-1):
        for j in range(i+1,len(Letters)):
            swaps.append(Letters[i] + Letters[j])
    
    Tree.mSwapPatterns = swaps
    
    # Openup file
    with open(message_filename, 'r') as file:
        contents = file.read()
    
    Tree.mRoot.AssignState(contents)
    
    # Call algorithms here ---------------------------------------------------
    
    
    
    return ''

c = task5("ssssssnnnnnooooaaatte")