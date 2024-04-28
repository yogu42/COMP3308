# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:40:43 2024

@author: Thomas
"""
import itertools
import string
from Node import *
import math

class CSearchParams:
    # Public class, all members accessible
    def __init__(self):
        self.mPathCost = 0
        self.mExpandedNodes = 0
        self.mMaxFringeSize = 0
        self.mDepth = 0
        
        # Some Constants
        self.mMaxDepth = 999
        self.mAllKeys = ""
        # Key
        self.mKey = []
    
    def GetFinalKey(self):
        # for k in range(1,len(self.mKey)):
        #     self.mAllKeys += self.mKey[k]
        self.mAllKeys = "".join(self.mKey[1:])
            
    def AddKey(self,aKeyList):
        self.mKey = aKeyList
        
    def AddPathCost(self,aKeyList):
        if isinstance(aKeyList, list):
            self.mPathCost = len(self.mKey)-1
            
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
        PrintOut = ""
        l2 = f"Num nodes expanded: {self.mExpandedNodes}\n"
        l3 = f"Max fringe size: {self.mMaxFringeSize}\n"
        l4 = f"Max depth: {self.mDepth}"
        
        PrintOut =  l2  + l3 + l4
        return PrintOut

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
        self.mFlagGreedy = "g"
        self.mFlagAStart = "a"
        
        # I/O messages and dictionary
        # Threshold
        self.mInputMsg = None
        self.mFinalOutputMsg = False
        self.mCurrentDecodedMsgs = None
        self.mPossibleMsg = []
        self.mDict = []
        self.mThreshold = 0
        self.mSearchParams = CSearchParams()
        
        # Swap combos and tree structure
        self.mSwaps =[]
        self.mTree = CTree()
        
        # Some constants
        self.mExpandLimit = 1000
        self.mDebugMsgsLen = 10
    
        # messages
        self.mNoSolution = "No solution found.\n\n"
        self.mFinalKey = ""
    
    def Heuristics(self,aNode):
        if self.ValidateDecodedMsgs(aNode.mState):
            aNode.mHeuristics = 0
            return 0
        
        else:
            self.mPossibleMsg.append(aNode.mState)
            MsgCopy = aNode.mState.upper()
            #MsgCopy.upper()
            
        
            Text = "ETAONS"
            FreqCount = {l: 0 for l in Text}  # Initialize FreqCount dictionary
            
            for char in MsgCopy:
                if char in Text:
                    FreqCount[char] += 1
            
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
            for charText,charSorted in zip(Text,SortedStr):
                if charSorted != charText:
                    MisplaceCount += 1 
            
            # Calculate heuristic
            Heuristic = math.ceil(MisplaceCount/2)
            aNode.mHeuristics = Heuristic
            
            return Heuristic

    def GetInputMsg(self,aFilename):
        try:
            with open(aFilename, 'r') as file:
                self.mInputMsg = file.read()
                
                self.mTree.mRoot.AssignState(self.mInputMsg)
                #self.mCurrentDecodedMsgs = self.mInputMsg
        except:
            print("Cannot open file ",aFilename)
    
    def GetDictionary(self,aDictFile):
        # Get all words from the dictionary
        with open(aDictFile, 'r') as file:
            content = file.read()
        self.mDict = content.split('\n')
    
    def GenerateSwapCombo(self,aLetters):
        Letters = list(aLetters)
        Letters.sort()
        # Generate all swap patterns
        for i in range(len(Letters)-1):
            for j in range(i+1,len(Letters)):
                self.mSwaps.append(Letters[i] + Letters[j])
        
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
            if MsgWord.lower() in self.mDict:
                ValidWordCount += 1
         
        Percentage = round(ValidWordCount/len(MsgsWordsList), 4) * 100

        IsMsgValid = True if Percentage >= self.mThreshold else False
        return IsMsgValid
    
    def DFS(self):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        depth = 0
        
        while Fringe and self.mSearchParams.mExpandedNodes < 1000:
            CurrentNode = Fringe.pop()
            
            Expanded.append(CurrentNode)
            self.mSearchParams.GetDepth(CurrentNode.mDepth)
            self.mSearchParams.ExpandedNodesSize(Expanded)
            
            if self.ValidateDecodedMsgs(CurrentNode.mState):
            # Record final messages
                self.mPossibleMsg.append(CurrentNode.mState)
                self.mFinalOutputMsg = CurrentNode.mState
                       
                # Get final key combinations
                KeyList = CurrentNode.BackTrack()
                       
                 # Record metrics
                self.mSearchParams.GetDepth(depth)
                self.mSearchParams.ExpandedNodesSize(Expanded)
                self.mSearchParams.GetMaxFringeSize(len(Fringe))
                self.mSearchParams.AddKey(KeyList)
                self.mSearchParams.AddPathCost(KeyList)
                self.mSearchParams.GetFinalKey()
                       
                break
            
            else:
                self.mPossibleMsg.append(CurrentNode.mState)
                
                #Generate new children
                NewChildren = self.mTree.GenerateChildNodes(CurrentNode)  
                NewChildren.reverse()
                depth += 1
                Fringe.extend(NewChildren)
                    
                self.mSearchParams.GetMaxFringeSize(len(Fringe))

    
    def BFS(self):
        Fringe = [self.mTree.ReturnRoot()]
        Expanded = []
        ExpandedKeys = []
        
        while Fringe:
            if self.mSearchParams.mExpandedNodes  >= self.mExpandLimit:
                break
            # Pop fringe
            CurrentNode = Fringe.pop(0)
            
            # Add to exanded
            Expanded.append(CurrentNode)
            #ExpandedKeys.append(CurrentNode.GetValue())
            
            # Get current depth
            self.mSearchParams.GetDepth(CurrentNode.mDepth)
            
            if self.ValidateDecodedMsgs(CurrentNode.mState):
                # Record final messages
                self.mPossibleMsg.append(CurrentNode.mState)
                self.mFinalOutputMsg = CurrentNode.mState
                
                # Get final key combinations
                KeyList = CurrentNode.BackTrack()
                
                # Record metrics
                self.mSearchParams.ExpandedNodesSize(Expanded)
                self.mSearchParams.GetMaxFringeSize(len(Fringe))
                self.mSearchParams.AddKey(KeyList)
                self.mSearchParams.AddPathCost(KeyList)
                self.mSearchParams.GetFinalKey()
                break
            
            else:
                self.mPossibleMsg.append(CurrentNode.mState)
                
                # Generate new children
                NewChildren = self.mTree.GenerateChildNodes(CurrentNode)
                
                # Add children to fringe
                Fringe.extend(NewChildren)
                # Record metrics
                self.mSearchParams.ExpandedNodesSize(Expanded)
                self.mSearchParams.GetMaxFringeSize(len(Fringe))
            
    def UCS(self):
        self.BFS()


    def IDS(self):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        ExpandedKeys = []
        depth = 0
        FringeKeys = []
        
        while self.mSearchParams.mExpandedNodes < 1000:
            
            for i in Fringe:
                FringeKeys.append(i.GetValue())
            CurrentNode = Fringe.pop(0)
            
            # add to expand
            Expanded.append(CurrentNode)
            ExpandedKeys.append(CurrentNode.GetValue())

            self.mSearchParams.GetDepth(CurrentNode.mDepth)
            self.mSearchParams.ExpandedNodesSize(Expanded)
            
            if self.ValidateDecodedMsgs(CurrentNode.mState):
            # Record final messages
                self.mPossibleMsg.append(CurrentNode.mState)
                self.mFinalOutputMsg = CurrentNode.mState
                       
                # Get final key combinations
                KeyList = CurrentNode.BackTrack()
                       
                  # Record metrics
                self.mSearchParams.GetDepth(CurrentNode.mDepth)
                self.mSearchParams.ExpandedNodesSize(Expanded)
                self.mSearchParams.GetMaxFringeSize(len(Fringe)-1)
                self.mSearchParams.AddKey(KeyList)
                self.mSearchParams.AddPathCost(KeyList)
                self.mSearchParams.GetFinalKey()
                       
                break
            
            else:
                self.mPossibleMsg.append(CurrentNode.mState)
                if CurrentNode.mDepth == depth:
                    
                    if not Fringe:
                        Fringe.append(self.mTree.mRoot)  
                        
                        depth += 1
                        
                    else:
                        Fringe.append(self.mTree.mRoot)
                        Fringe.append(CurrentNode)
                        
                        if not CurrentNode.mChildNodes:
                            self.mTree.GenerateChildNodes(CurrentNode)
                            Fringe.extend(CurrentNode.mChildNodes)     
                    
                        

                elif CurrentNode.mDepth < depth:
                    if not CurrentNode.mChildNodes:
                        self.mTree.GenerateChildNodes(CurrentNode)
                        Fringe.extend(CurrentNode.mChildNodes)
                        
                    # if not Fringe:
                    #     #Fringe.append(self.mTree.mRoot)
                    #     Fringe.extend(CurrentNode.mChildNodes)
            
            print(FringeKeys)
    
    def Greedy(self):
        Fringe = [self.mTree.ReturnRoot()]
        Expanded = []
        while Fringe:
            CurrentNode = Fringe.pop(0)
            
            Expanded.append(CurrentNode)
            if len(Expanded) > 1000:
                break
            self.mSearchParams.GetDepth(CurrentNode.mDepth)
            self.mSearchParams.ExpandedNodesSize(Expanded)

            if self.Heuristics(CurrentNode) == 0:
                self.mPossibleMsg.append(CurrentNode.mState)
                self.mFinalOutputMsg = CurrentNode.mState
                
                KeyList = CurrentNode.BackTrack()
                
                self.mSearchParams.GetMaxFringeSize(len(Fringe))
                self.mSearchParams.AddKey(KeyList)
                self.mSearchParams.AddPathCost(KeyList)
                self.mSearchParams.GetFinalKey()
                break
            
            else:
                NewChildren = self.mTree.GenerateChildNodes(CurrentNode)
                H = [self.Heuristics(node) for node in NewChildren]
                
                MinNode = H.index(min(H))
                CurrentNode = NewChildren[MinNode]
                NewChildren.pop(MinNode)
                
                Fringe.append(CurrentNode)
                #Fringe.extend(NewChildren)
                
                self.mSearchParams.GetMaxFringeSize(len(Fringe))


    def BlindSearch(self,aAlgo, aMsgFile, aDictFile, aThresh,aLetters, aDebug):
        # Read input file
        self.GetInputMsg(aMsgFile)
        
        # Get swap combos
        self.GenerateSwapCombo(aLetters)
        
        # Read dictionary file
        self.GetDictionary(aDictFile)
        
        # Set threshold
        self.mThreshold = aThresh
        
        Keys = None
        # Determine algorithm
        if aAlgo == self.mFlagDFS:
            self.DFS()
        
        elif aAlgo == self.mFlagBFS:
            self.BFS()
        
        elif aAlgo == self.mFlagUCS:
            self.UCS()
        
        elif aAlgo == self.mFlagIDS:
            self.IDS()
            
        elif aAlgo == self.mFlagGreedy:
            self.Greedy()
        
        FinalOutput = ""
        
        if self.mFinalOutputMsg:
            PrintOut = f"Solution: {self.mFinalOutputMsg}\n\n"
            AllKey = "Key: " + self.mSearchParams.mAllKeys + "\n"
            PathCost = f"Path Cost: {self.mSearchParams.mPathCost}\n\n"
            SearchParamStr = self.mSearchParams.PrintOutMetrics()
            
            if aDebug == "y":
                DebugMsg = "First few expanded states:\n"
                if (len(self.mPossibleMsg) < self.mDebugMsgsLen):
                    for i in range(len(self.mPossibleMsg)):
                        if i < len(self.mPossibleMsg)-1:
                            DebugMsg += self.mPossibleMsg[i] + "\n\n"
                        else:
                            DebugMsg += self.mPossibleMsg[i]
                    
                else:
                    for i in range(self.mDebugMsgsLen):
                        if i < self.mDebugMsgsLen-1:
                            DebugMsg += self.mPossibleMsg[i] + "\n\n"
                        else:
                            DebugMsg += self.mPossibleMsg[i]
                        
                FinalOutput = PrintOut + AllKey +PathCost + SearchParamStr + "\n\n" + DebugMsg
            else:
                FinalOutput = PrintOut + AllKey +PathCost + SearchParamStr
                
        else:
            PrintOut = f"No solution found.\n\n"
            SearchParamStr = self.mSearchParams.PrintOutMetrics()
            if aDebug == "y":
                DebugMsg = "First few expanded states:\n"
                if (len(self.mPossibleMsg) < self.mDebugMsgsLen):
                    for i in range(len(self.mPossibleMsg)):
                        if i < len(self.mPossibleMsg)-1:
                            DebugMsg += self.mPossibleMsg[i] + "\n\n"
                        else:
                            DebugMsg += self.mPossibleMsg[i]
                    
                else:
                    for i in range(self.mDebugMsgsLen):
                        if i < self.mDebugMsgsLen-1:
                            DebugMsg += self.mPossibleMsg[i] + "\n\n"
                        else:
                            DebugMsg += self.mPossibleMsg[i]
                        
                FinalOutput = PrintOut + SearchParamStr + "\n\n" + DebugMsg
            
            else:
                FinalOutput = PrintOut + SearchParamStr
            #FinalOutput = PrintOut + SearchParamStr 
        
        #----------------------------------------------------------------------
        return FinalOutput
                    
 
def task4(aAlgo, aMsgFile, aDictFile, aThresh,aLetters, aDebug):

    MsgEncoderObj = CMessageCoder()
    m = MsgEncoderObj.BlindSearch(aAlgo, aMsgFile, aDictFile, aThresh, aLetters, aDebug)

    return m

def task6(aAlgo, aMsgFile, aDictFile, aThresh,aLetters, aDebug):
    
    MsgEncoderObj = CMessageCoder()
    m = MsgEncoderObj.BlindSearch(aAlgo, aMsgFile, aDictFile, aThresh, aLetters, aDebug)

    return m
    
if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task4 function
    #print(task4('d', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    #print(task4('b', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    #print(task4('u', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'n'))
    print(task4('i', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y')) 
    #print(task4('i', 'cabs.txt', 'common_words.txt', 100, 'ADE', 'n')) 
   

    #print(task6('g', 'secret_msg.txt', 'common_words.txt', 90, 'AENOST', 'n'))
    

            



