# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 23:14:18 2024

@author: Thomas
"""
import math

def task5(message_filename, is_goal):
    if is_goal:
        return 0
    
    else:
        # open file
        with open(message_filename, 'r') as file:
            contents = file.read().upper()
        
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


if __name__ == '__main__':
  # Example function calls below, you can add your own to test the task5 function
  print(task5('ai.txt', False))
  print(task5('freq_eg1.txt', True))
  print(task5('freq_eg2.txt', False))
