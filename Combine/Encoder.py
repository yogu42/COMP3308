# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:40:43 2024

@author: Thomas
"""
import itertools
import string
from Node import CNode,CTree
from SearchTool import *

class CMessageCoder:
    def __init__(self):
        self.mEncodeMode = "e"
        self.mDecodeMode = "d"
        
        self.mInputMsg = None
        self.mFinalOutputMsg = ""
        self.mPossibleMsg = []
        self.mDict = []

        self.mSwaps =[]
        self.mTree = CTree()
        
        # Algorithm flags
        self.mFlagDFS = "d"
        self.mFlagBFS = "b"
        self.mFlagUCS = "u"
        self.mFlagIDS = "i"
        
        # Some constants
        self.mLimit = 1000
        self.mYesLimit = 10
        # messages
        self.mNoSolution = "No solution found.\n\n"
        self.mFinalKey = ""
       
    def GetInputMsg(self,aFilename):
        try:
            with open(aFilename, 'r') as file:
                self.mInputMsg = file.read()
        except:
            print("Cannot open file ",aFilename)

    def DecodeMessages(self,aKey):
        # Parse key, can only contatin 2 different letters
        if not isinstance(aKey, str):
            raise TypeError("Must be a string")
            
        if not (len(aKey) == 2):
            raise ValueError("STring must contain two letters only")
        else:
            if (aKey[0] == aKey[1]):
                raise ValueError("Swap keys must be different")
        
        # iterate through input message
        NewMsg = ""
        if isinstance(self.mInputMsg, str):
            for char in self.mInputMsg:
                IsSwapped = False
                NewChar = char
                
                # Swap letters 
                if aKey[1] == NewChar:
                    NewChar = aKey[0]
                    IsSwapped = True
                  
                elif aKey[1].lower() == NewChar :
                    NewChar  = aKey[0].lower()
                    IsSwapped = True
                  
                elif aKey[0] == NewChar:
                    NewChar  = aKey[1]
                    IsSwapped = True
                  
                elif aKey[0].lower() == NewChar:
                    NewChar = aKey[1].lower()
                    IsSwapped  = True
                
                # Construct new message
                if not IsSwapped:
                    NewMsg += char

                else:
                    NewMsg += NewChar
        
            # insert decoded messages
            self.mPossibleMsg.append(NewMsg)
        else:
            raise TypeError("No input message")
    
    def GenerateSwapCombo(self,aLetters):
        # Generate all swap patterns
        for i in range(len(aLetters)-1):
            newBranch = {aLetters[i]:[]}
            
            for j in range(i+1,len(aLetters)):
                newBranch[aLetters[i]].append(aLetters[j])
            
            self.mSwaps.append(newBranch)
        
        # Copy swap patterns 
        self.mTree.GetSwapPatterns(self.mSwaps)
    
    def CreateTree(self):
        self.mTree.GenerateStructure()
        
    
    def DFS(self):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        ExpandedKeys = []                       # List store expanded nodes' value
        aCostCount = 0
        
        def DFSRecursive(aNode):
            if (aNode not in Expanded) and (aNode.GetValue() not in ExpandedKeys):
                LeftChild = aNode.mLeftChild
                RightChild = aNode.mRightChild
                
                if LeftChild and LeftChild not in Expanded:
                    DFSRecursive(aNode.mLeftChild)
                    
                if RightChild and RightChild not in Expanded:
                    DFSRecursive(aNode.mRightChild)
                    
                Expanded.append(aNode)
                ExpandedKeys.append(aNode.GetValue())
                
        while Fringe:
            CurrentNode = Fringe.pop(0)
            # Main Decoding go here
            
            
            #---------------------
            
            DFSRecursive(CurrentNode)
        
        
        print(ExpandedKeys)
                
    def BFS(self):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        ExpandedKeys = []                       # List store expanded nodes' value
        PathCost = 0
        
        while Fringe:
            # Pop first node from fringe
            CurrentNode = Fringe.pop(0)
            
            if (CurrentNode not in Expanded) and (CurrentNode.GetValue() not in ExpandedKeys):
                LeftChild = CurrentNode.mLeftChild
                RightChild = CurrentNode.mRightChild
                
                # Main Decoding go here
                
                
                #---------------------
                
                # Add child nodes
                if LeftChild and LeftChild not in Expanded:
                    Fringe.append(LeftChild)
                
                if RightChild and RightChild not in Expanded:
                    Fringe.append(RightChild)
                    
                # Add current node to expanded
                Expanded.append(CurrentNode)
                ExpandedKeys.append(CurrentNode.GetValue())
                PathCost += 1
        
        print(ExpandedKeys)
                    
    def UCS(self):
        self.BFS()
        
    def IDS(self,aLimit):
        
        pass
    
    def BlindSearch(self,aAlgo, aMsgFile, aDictFile, aThresh,aLetters, aDebug):
        pass
    
    

m = CMessageCoder()
m.GenerateSwapCombo('ABCDE')
m.CreateTree()
m.GetInputMsg('spain.txt')
m.DecodeMessages("AE")
m.DFS()
m.BFS()
