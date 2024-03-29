# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:40:43 2024

@author: Thomas
"""
import itertools
import string
from Node import *

class CSearchParams:
    # Public class, all members accessible
    def __init__(self):
        self.mPathCost = 0
        self.mExpandedNodes = 0
        self.mMaxFringeSize = 0
        self.mDepth = 0
        
        # Some Constants
        self.mMaxDepth = 999
    
    def AddPathCost(self, aCost):
        self.mPathCost += aCost
    
    def ExpandedNodesSize(self, aExpandList):
        if isinstance(aExpandList,list):
            self.mExpandedNodes = len(aExpandList)
    
    def GetMaxFringeSize(self, aFringeSize):
        if isinstance(aFringeSize,int):
            if aFringeSize > self.mMaxFringeSize:
                self.mMaxFringeSize = aFringeSize
    
    def GetDepth (self,aDepth):
        if isinstance(aDepth,int):
            self.mDepth = aDepth    
    

class CMessageCoder:
    def __init__(self):
        # Encode/Decode flags
        self.mEncodeMode = "e"
        self.mDecodeMode = "d"
        
        # Algorithm flags
        self.mFlagDFS = "d"
        self.mFlagBFS = "b"
        self.mFlagUCS = "u"
        self.mFlagIDS = "i"
            
        # I/O messages and dictionary
        # Threshold
        self.mInputMsg = None
        self.mFinalOutputMsg = ""
        self.mPossibleMsg = []
        self.mDict = []
        self.mThreshold = 0
        self.mSearchParams = CSearchParams()
        
        # Swap combos and tree structure
        self.mSwaps =[]
        self.mTree = CTree()
        
        # Some constants
        self.mDepthLimit = 1000
        self.mDebugMsgsLen = 10
    
        # messages
        self.mNoSolution = "No solution found.\n\n"
        self.mFinalKey = ""
        
    def CreateTree(self):
        self.mTree.GenerateStructure()
    
    def CountDepth(self,aNode):
        # Get ket of current node
        Key = aNode.GetValue()
        FirstLetterList = []
        LstOfLetter2 = []
        # First letter index + Second letter index = depth
        First = 0
        Second = 0
        for combo in self.mSwaps:
            # Get all First Letters into a list and use their indices later
            k = next(iter(combo))
            FirstLetterList.append(k)
            
            # Get all list of combinitation using the first letter key
            LstOfLetter2.append(combo[k])
              
        # Getthe indices
        First = FirstLetterList.index(Key[0])
        Second = LstOfLetter2[First].index(Key[1])
        
        Depth = First + Second
        
        return Depth

    
    def GetInputMsg(self,aFilename):
        try:
            with open(aFilename, 'r') as file:
                self.mInputMsg = file.read()
        except:
            print("Cannot open file ",aFilename)
    
    def GetDictionary(self,aDictFile):
        # Get all words from the dictionary
        with open(aDictFile, 'r') as file:
          for line in file:
            CleanLine = line.rstrip()
            self.mDict.append(CleanLine)
            
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
            
            return NewMsg
        else:
            return False
    
    def GenerateSwapCombo(self,aLetters):
        # Generate all swap patterns
        for i in range(len(aLetters)-1):
            newBranch = {aLetters[i]:[]}
            
            for j in range(i+1,len(aLetters)):
                newBranch[aLetters[i]].append(aLetters[j])
            
            self.mSwaps.append(newBranch)
        
        # Copy swap patterns 
        self.mTree.GetSwapPatterns(self.mSwaps)
    
    
    def ValidateDecodedMsgs(self):
       
        # Remove all symbols
        Symbols = string.punctuation
        
        # Create a translation table. Third argument is the string of symbols to remove.
        TransTab = self.mInputMsg.maketrans('', '', Symbols)
        
        # Remove all symbols from input message
        CleanMsg = self.mInputMsg.translate(TransTab)
        
        # Turn the input message into a lists of words
        MsgsWordsList = CleanMsg.split()
        
        # Check percentage of word
        ValidWordCount = 0
        for MsgWord in MsgsWordsList:
            for Word in self.mDict:
                if MsgWord.lower() == Word.lower():
                    ValidWordCount += 1
        
        Percentage = round(ValidWordCount/len(CleanMsg), 4) * 100
        IsMsgValid = True if Percentage >= self.mThreshold else False
        
        return IsMsgValid

    
    def DFS(self):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        ExpandedKeys = []                       # List store expanded nodes' value
        
        def DFSRecursive(aNode):
            #print(aNode.GetValue())
            self.mSearchParams.GetDepth(self.CountDepth(aNode))
            if (aNode not in Expanded) :
                LeftChild = aNode.mLeftChild
                RightChild = aNode.mRightChild
                
                if LeftChild and LeftChild not in Expanded:
                    Fringe.append(LeftChild)
                    DFSRecursive(aNode.mLeftChild)
                    
                if RightChild and RightChild not in Expanded:
                    Fringe.append(RightChild)
                    DFSRecursive(aNode.mRightChild)
                    
                Expanded.append(aNode)

        while Fringe:
            CurrentNode = Fringe.pop(0)

            ExpandedKeys.append(CurrentNode.GetValue())
            # Main Decoding go here: Decode message
            Key = CurrentNode.GetValue()
            NewMsg = self.DecodeMessages(Key)
            
            # If message is successfully decode. Validify the message
            if NewMsg:
                IsMsgDecoded = self.ValidateDecodedMsgs()
                if IsMsgDecoded:
                    break
                else:
                    continue
            #---------------------
            DFSRecursive(CurrentNode)
            
        print(ExpandedKeys)

    def BFS(self):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        ExpandedKeys = []                       # List store expanded nodes' value
        
        while Fringe:
            # Pop first node from fringe
            CurrentNode = Fringe.pop(0)
            
            # Get Current Depth
            self.mSearchParams.GetDepth(self.CountDepth(CurrentNode))
            
            # Get Current Fring Size
            
            if (CurrentNode not in Expanded) and (CurrentNode.GetValue() not in ExpandedKeys):
                LeftChild = CurrentNode.mLeftChild
                RightChild = CurrentNode.mRightChild
                
                # Main Decoding go here
                Key = CurrentNode.GetValue()
                NewMsg = self.DecodeMessages(Key)
                
                # If message is successfully decode. Validify the message
                if NewMsg:
                    IsMsgDecoded = self.ValidateDecodedMsgs()
                    
                    if IsMsgDecoded:
                        break
                    else:
                        continue
                #---------------------
                
                # Add child nodes
                if LeftChild and LeftChild not in Expanded:
                    Fringe.append(LeftChild)
                
                if RightChild and RightChild not in Expanded:
                    Fringe.append(RightChild)
                    
                # Add current node to expanded
                Expanded.append(CurrentNode)
                ExpandedKeys.append(CurrentNode.GetValue())
        print(ExpandedKeys)
        
    def UCS(self):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        ExpandedKeys = []                       # List store expanded nodes' value
        
        while Fringe:
            # Pop first node from fringe
            CurrentNode = Fringe.pop(0)
            self.mSearchParams.GetDepth(self.CountDepth(CurrentNode))
            if (CurrentNode not in Expanded) and (CurrentNode.GetValue() not in ExpandedKeys):
                LeftChild = CurrentNode.mLeftChild
                RightChild = CurrentNode.mRightChild
                
                # Main Decoding go here
                Key = CurrentNode.GetValue()
                NewMsg = self.DecodeMessages(Key)
                
                # If message is successfully decode. Validify the message
                # if NewMsg:
                #     IsMsgDecoded = self.ValidateDecodedMsgs()
                    
                #     if IsMsgDecoded:
                #         break
                #     else:
                #         continue
                #---------------------
                
                # Add child nodes
                if LeftChild and RightChild:
                    LeftCost = LeftChild.mCost
                    RightCost = RightChild.mCost
                    
                    # if Cost is the same, go left
                    
                    if (LeftCost < RightCost):
                        if RightChild and RightChild not in Expanded:
                            Fringe.append(RightChild)
                        
                        if LeftChild and LeftChild not in Expanded:
                            Fringe.append(LeftChild)
                    else:
                        if LeftChild and LeftChild not in Expanded:
                            Fringe.append(LeftChild)
                    
                        if RightChild and RightChild not in Expanded:
                            Fringe.append(RightChild)
                elif LeftChild:
                    Fringe.append(LeftChild)
                    
                elif RightChild:
                    Fringe.append(RightChild)
                    # Add current node to expanded
                Expanded.append(CurrentNode)
                ExpandedKeys.append(CurrentNode.GetValue())
                
        print(ExpandedKeys)
        
    def IDS(self,aLimit = 999):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        ExpandedKeys = []  
        
        def DFSLimit(aNode,aDepthLimit):
            self.mSearchParams.GetDepth(self.CountDepth(aNode))
            if self.mSearchParams.mDepth < aDepthLimit:
                
                LeftChild = aNode.mLeftChild
                RightChild = aNode.mRightChild

                if LeftChild and LeftChild not in Fringe:
                    Fringe.append(LeftChild)
                    DFSLimit(aNode.mLeftChild,aDepthLimit)
                    
                if RightChild and RightChild not in Fringe:
                    Fringe.append(RightChild)
                    DFSLimit(aNode.mRightChild,aDepthLimit)
                
                Expanded.append(aNode)
                

        while Fringe:
            # Pop first node from fringe
            CurrentNode = Fringe.pop(0)
            ExpandedKeys.append(CurrentNode.GetValue())
            Key = CurrentNode.GetValue()
            NewMsg = self.DecodeMessages(Key)
            
            # If message is successfully decode. Validify the message
            if NewMsg:
                IsMsgDecoded = self.ValidateDecodedMsgs()
                if IsMsgDecoded:
                    break
                else:
                    continue
            
            DFSLimit(CurrentNode, aLimit)


    def BlindSearch(self,aAlgo, aMsgFile, aDictFile, aThresh,aLetters, aDebug):
        pass
    
m = CMessageCoder()
m.GenerateSwapCombo("ABCDE")
m.CreateTree()

m.UCS()



