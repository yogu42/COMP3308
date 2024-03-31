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
    
    def PrintOutMetrics(self):
        print(f"Path Cost: {self.mPathCost}\n")
        print(f"Num nodes expanded: {self.mExpandedNodes}")
        print(f"Max fringe size: {self.mMaxFringeSize}")
        print(f"Max depth: {self.mDepth}\n")

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
        self.mFinalOutputMsg = None
        self.mPossibleMsg = []
        self.mDict = []
        self.mThreshold = 0
        self.mSearchParams = CSearchParams()
        
        # Swap combos and tree structure
        self.mSwaps =[]
        self.mTree = CTree()
        
        # Some constants
        self.mDepthLimit = 1000
        self.mFringeLimit = 2001
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
        Letters = list(aLetters)
        Letters.sort()
        # Generate all swap patterns
        for i in range(len(Letters)-1):
            newBranch = {Letters[i]:[]}
            
            for j in range(i+1,len(Letters)):
                newBranch[Letters[i]].append(Letters[j])
            
            self.mSwaps.append(newBranch)
        
        # Copy swap patterns 
        self.mTree.GetSwapPatterns(self.mSwaps)
    
    def ValidateDecodedMsgs(self, aMsg):
       
        # Remove all symbols
        Symbols = string.punctuation
        
        # Create a translation table. Third argument is the string of symbols to remove.
        TransTab =  aMsg.maketrans('', '', Symbols)
        
        # Remove all symbols from input message
        CleanMsg =  aMsg.translate(TransTab)
        
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
            if len(Expanded) >= self.mDepthLimit:
                break
            
            CurrentNode = Fringe.pop(0)
            
            #Get current fringe size
            self.mSearchParams.GetMaxFringeSize(len(Fringe))
            
            ExpandedKeys.append(CurrentNode.GetValue())
            # Main Decoding go here: Decode message
            Key = CurrentNode.GetValue()
            NewMsg = self.DecodeMessages(Key)
            
            # If message is successfully decode. Validify the message
            if NewMsg:
                IsMsgDecoded = self.ValidateDecodedMsgs(NewMsg)
                if IsMsgDecoded:
                    self.mFinalOutputMsg = NewMsg
                    break
                
                else:
                    self.mPossibleMsg.append(NewMsg)
                    
            #---------------------
            DFSRecursive(CurrentNode)
            
        # Get number of expanded nodes
        self.mSearchParams.ExpandedNodesSize(Expanded)
        
        return ExpandedKeys

    def BFS(self):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        ExpandedKeys = []                       # List store expanded nodes' value
        
        while Fringe:
            if len(Expanded) >= self.mDepthLimit:
                break
            
            #Get current fringe size
            self.mSearchParams.GetMaxFringeSize(len(Fringe))
            
            # Pop first node from fringe
            CurrentNode = Fringe.pop(0)
            
            # Get Current Depth
            self.mSearchParams.GetDepth(self.CountDepth(CurrentNode))
            
            if (CurrentNode not in Expanded) and (CurrentNode.GetValue() not in ExpandedKeys):
                LeftChild = CurrentNode.mLeftChild
                RightChild = CurrentNode.mRightChild
                
                # Main Decoding go here
                Key = CurrentNode.GetValue()
                NewMsg = self.DecodeMessages(Key)

                #If message is successfully decode. Validify the message
                if NewMsg:
                    IsMsgDecoded = self.ValidateDecodedMsgs(NewMsg)

                    if IsMsgDecoded:
                        self.mFinalOutputMsg = NewMsg
                        break
                    
                    else:
                        self.mPossibleMsg.append(NewMsg)
                        
                #---------------------
                
                # Add child nodes
                if LeftChild and LeftChild not in Expanded:
                    Fringe.append(LeftChild)
                
                if RightChild and RightChild not in Expanded:
                    Fringe.append(RightChild)
                    
                # Add current node to expanded
                Expanded.append(CurrentNode)
                ExpandedKeys.append(CurrentNode.GetValue())
                
        # Get number of expanded nodes
        self.mSearchParams.ExpandedNodesSize(Expanded)
        
        return ExpandedKeys
        
    def UCS(self):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        ExpandedKeys = []                       # List store expanded nodes' value
        
        while Fringe:
            if len(Expanded) >= self.mDepthLimit:
                break
            
            #Get current fringe size
            self.mSearchParams.GetMaxFringeSize(len(Fringe))
            
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
                if NewMsg:
                    IsMsgDecoded = self.ValidateDecodedMsgs(NewMsg)
                    if IsMsgDecoded:
                        self.mFinalOutputMsg = NewMsg
                        break
                    
                    else:
                        self.mPossibleMsg.append(NewMsg)
                        
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
                
        # Get number of expanded nodes
        self.mSearchParams.ExpandedNodesSize(Expanded)
        
        return ExpandedKeys
        
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
            if len(Expanded) >= self.mDepthLimit:
                break
            #Get current fringe size
            self.mSearchParams.GetMaxFringeSize(len(Fringe))
            
            # Pop first node from fringe
            CurrentNode = Fringe.pop(0)
            
            ExpandedKeys.append(CurrentNode.GetValue())
            
            Key = CurrentNode.GetValue()
            NewMsg = self.DecodeMessages(Key)
            # MAin Processing -----------------------------
            
            
            # If message is successfully decode. Validify the message
            if NewMsg:
                IsMsgDecoded = self.ValidateDecodedMsgs(NewMsg)
                if IsMsgDecoded:
                    self.mFinalOutputMsg = NewMsg
                    break
                
                else:
                    self.mPossibleMsg.append(NewMsg)
            
            DFSLimit(CurrentNode, aLimit)
        
        # Get number of expanded nodes
        self.mSearchParams.ExpandedNodesSize(Expanded)
        
        return ExpandedKeys

    def BlindSearch(self,aAlgo, aMsgFile, aDictFile, aThresh,aLetters, aDebug):
        # Read input file
        self.GetInputMsg(aMsgFile)
        
        # Get swap combos
        self.GenerateSwapCombo(aLetters)
        
        # Create Tree Structure
        self.CreateTree()
        
        # Read dictionary file
        self.GetDictionary(aDictFile)
        
        # Set threshold
        self.mThreshold = aThresh
        
        Keys = None
        # Determine algorithm
        if aAlgo == self.mFlagDFS:
            Keys = self.DFS()
        
        elif aAlgo == self.mFlagBFS:
            Keys =self.BFS()
        
        elif aAlgo == self.mFlagUCS:
            Keys =self.UCS()
        
        elif aAlgo == self.mFlagIDS:
            Keys =self.IDS()
        
        # Print out metrix 
        # Check if a final solution has been found
        if self.mFinalOutputMsg:
            print(self.mFinalOutputMsg)
        
        else:
            print(self.mPossibleMsg)
           
            
def task4(aAlgo, aMsgFile, aDictFile, aThresh,aLetters, aDebug):
    MsgEncoderObj = CMessageCoder()
    print(MsgEncoderObj.mSwaps)
    MsgEncoderObj.BlindSearch(aAlgo, aMsgFile, aDictFile, aThresh, aLetters, aDebug)
    return MsgEncoderObj
    
# if __name__ == '__main__':
#     # Example function calls below, you can add your own to test the task4 function
#     print(task4('d', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
#     print(task4('b', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
#     print(task4('i', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))        
            


m = CMessageCoder()
m.GenerateSwapCombo("ABCDEFG")
m.CreateTree()
m.GetInputMsg("fruit_ode.txt")
m.GetDictionary("dict_fruit.txt")
m.mThreshold = 100.0
BFS = m.DFS()
#print(m.mPossibleMsg)



