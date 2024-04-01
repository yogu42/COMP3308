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
        self.mAllKeys = ""
        # Key
        self.mKey = []
    
    def GetFinalKey(self):
        for k in range(1,len(self.mKey)):
            self.mAllKeys += self.mKey[k]
            
    def AddKey(self,aKeyList):
        self.mKey = aKeyList
        
    def AddPathCost(self,aKeyList):
        if isinstance(aKeyList, list):
            self.mPathCost = len(self.mKey) - 1
            
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

        #l0 = f"Key: {AllKeys}\n"
        #l1 = f"Path Cost: {self.mPathCost}\n\n"
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
    
    def CountDepth(self,aNode):
        # Get ket of current node
        pass

    def GetInputMsg(self,aFilename):
        try:
            with open(aFilename, 'r') as file:
                self.mInputMsg = file.read()
                
                self.mCurrentDecodedMsgs = self.mInputMsg
        except:
            print("Cannot open file ",aFilename)
    
    def GetDictionary(self,aDictFile):
        # Get all words from the dictionary
        with open(aDictFile, 'r') as file:
            content = file.read()
        self.mDict = content.split('\n')

    def DecodeMessages(self,aKeyList):
        if isinstance(self.mInputMsg, str):
            if len(aKeyList) == 1:
                self.mPossibleMsg.append(self.mInputMsg)
                self.mCurrentDecodedMsgs = self.mInputMsg
                
                return self.mInputMsg
            
            elif len(aKeyList) == 2:
                swap = aKeyList[1]
                msg = list(self.mInputMsg)
                
                for i in range(len(msg)):
                    if msg[i] == swap[0].lower():
                        msg[i] = swap[1].lower()
                            
                    elif msg[i] == swap[0]:
                        msg[i] = swap[1]
                            
                    elif msg[i] == swap[1].lower():
                        msg[i] = swap[0].lower()
                            
                    elif msg[i] == swap[1]:
                        msg[i] = swap[0]
                
                NewMsg = "".join(msg)
                #self.mCurrentDecodedMsgs = NewMsg
                
                self.mPossibleMsg.append(NewMsg)
                return NewMsg
                        
            elif len(aKeyList) > 2:
                self.mCurrentDecodedMsgs = self.mInputMsg
                for swap in aKeyList:
                    msg = list(self.mCurrentDecodedMsgs)
                    for i in range(len(msg)):
                        if msg[i] == swap[0].lower():
                            msg[i] = swap[1].lower()
                                
                        elif msg[i] == swap[0]:
                            msg[i] = swap[1]
                                
                        elif msg[i] == swap[1].lower():
                            msg[i] = swap[0].lower()
                                
                        elif msg[i] == swap[1]:
                            msg[i] = swap[0]
                            
                    NewMsg = "".join(msg)
                    self.mCurrentDecodedMsgs = NewMsg
                    
                self.mPossibleMsg.append(self.mCurrentDecodedMsgs)
                
                return self.mCurrentDecodedMsgs
        else:
            return False
    
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
        ExpandedKeys = []                       # List store expanded nodes' value
    
        
        def DFSNoLimit(aNode):
            if self.mSearchParams.mExpandedNodes  >= self.mExpandLimit:
                return
            
            self.mSearchParams.GetDepth(aNode.mDepth)
            
            # Get depth and cost of expanded node
            NodeKey = aNode.GetValue()
            #KeyList = aNode.BackTrack()
            
            Expanded.append(aNode)
            ExpandedKeys.append(NodeKey)
            
            self.mSearchParams.ExpandedNodesSize(Expanded)
            
            # Main decoding--------------------
            # Decode all ccombintations
            NewMsgs = self.DecodeMessages(ExpandedKeys)
            
            if NewMsgs:
                # Validate the message IF True stop
                if self.ValidateDecodedMsgs(NewMsgs):
                    self.mSearchParams.AddKey(KeyList)
                    self.mFinalOutputMsg = NewMsgs

                    # Record path cost
                    self.mSearchParams.AddPathCost(KeyList)

                    return 
                
                # If not generate children
                else:
                    NewChildren = self.mTree.GenerateChildNodes(aNode)
                    self.mSearchParams.GetMaxFringeSize(len(Fringe) + len(NewChildren))
                    
                    NewNode = NewChildren.pop(0)  
                    
                    
                    # Check if depth is larger or equal to cancel expansion
                    if self.mSearchParams.mDepth >= 999:
                        return 
                    
                    Fringe.extend(NewChildren)

                    DFSNoLimit(NewNode)
                
                    
        while Fringe:
            CurrentNode = Fringe.pop(0)
            self.mSearchParams.GetDepth(CurrentNode.mDepth)
            DFSNoLimit(CurrentNode)

        return ExpandedKeys

    def BFS(self):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        ExpandedKeys = []                       # List store expanded nodes' value
        
        self.mSearchParams.GetDepth(0)
        self.mSearchParams.GetMaxFringeSize(len(Fringe))
        
        while Fringe:
            if self.mSearchParams.mExpandedNodes >= self.mExpandLimit:
                break
            
            # Pop current node out of the fringe  get the key list
            CurrentNode = Fringe.pop(0)
            CurrentKey = CurrentNode.GetValue()
            KeyList = CurrentNode.BackTrack()
            
            # Get depth and cost of expanded node
            self.mSearchParams.GetDepth(CurrentNode.mDepth)
             
            Expanded.append(CurrentNode)
            ExpandedKeys.append(CurrentKey)
  
            # Main decoding--------------------
            # Decode all ccombintations
            NewMsgs = self.DecodeMessages(KeyList)
            self.mSearchParams.AddKey(KeyList)
            
            # Record path cost
            self.mSearchParams.AddPathCost(KeyList)
            if NewMsgs:
                # Validate the message IF True stop
                if self.ValidateDecodedMsgs(NewMsgs):
                    self.mFinalOutputMsg = NewMsgs
                    
                    # Record sizes of Expanded, Fringe and depth value
                    self.mSearchParams.ExpandedNodesSize(Expanded)

                    # Get final key
                    self.mSearchParams.GetFinalKey()
                    break
                
                # If not generate children
                else:
                    NewChildren = self.mTree.GenerateChildNodes(CurrentNode)
                    
                    # Generate new children
                    Fringe.extend(NewChildren)

                    # Record sizes of Expanded, Fringe and depth value
                    self.mSearchParams.ExpandedNodesSize(Expanded)
                    self.mSearchParams.GetMaxFringeSize(len(Fringe))

        return ExpandedKeys
        
    def UCS(self):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        ExpandedKeys = []                       # List store expanded nodes' value
        
        self.mSearchParams.GetDepth(0)
        self.mSearchParams.GetMaxFringeSize(len(Fringe))
        
        while Fringe:
            if self.mSearchParams.mExpandedNodes >= self.mExpandLimit:
                break
            
            # Pop current node out of the fringe  get the key list
            CurrentNode = Fringe.pop(0)
            CurrentKey = CurrentNode.GetValue()
            KeyList = CurrentNode.BackTrack()
            
            # Get depth and cost of expanded node
            self.mSearchParams.GetDepth(CurrentNode.mDepth)
             
            Expanded.append(CurrentNode)
            ExpandedKeys.append(CurrentKey)
  
            # Main decoding--------------------
            # Decode all ccombintations
            NewMsgs = self.DecodeMessages(KeyList)
            self.mSearchParams.AddKey(KeyList)
            
            # Record path cost
            self.mSearchParams.AddPathCost(KeyList)
            if NewMsgs:
                # Validate the message IF True stop
                if self.ValidateDecodedMsgs(NewMsgs):
                    self.mFinalOutputMsg = NewMsgs
                    
                    # Record sizes of Expanded, Fringe and depth value
                    self.mSearchParams.ExpandedNodesSize(Expanded)

                    # Get final key
                    self.mSearchParams.GetFinalKey()
                    break
                
                # If not generate children
                else:
                    NewChildren = self.mTree.GenerateChildNodes(CurrentNode)
                    
                    # Generate new children
                    Fringe.extend(NewChildren)

                    # Record sizes of Expanded, Fringe and depth value
                    self.mSearchParams.ExpandedNodesSize(Expanded)
                    self.mSearchParams.GetMaxFringeSize(len(Fringe))

        return ExpandedKeys
        
    def IDS(self,aLimit = 999):
        Fringe = [self.mTree.ReturnRoot()]      # List store nodes  in fringe
        Expanded = []                           # List store expanded nodes
        ExpandedKeys = []  
        
        def DFSLimit(aNode,aDepthLimit):
            self.mSearchParams.GetDepth(self.CountDepth(aNode))
            if self.mSearchParams.mDepth < aDepthLimit:
                Expanded.append(aNode)
  
        return ExpandedKeys

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
            Keys = self.DFS()
        
        elif aAlgo == self.mFlagBFS:
            Keys =self.BFS()
        
        elif aAlgo == self.mFlagUCS:
            Keys =self.UCS()
        
        elif aAlgo == self.mFlagIDS:
            Keys =self.IDS()
        
        FinalOutput = ""
        
        if self.mFinalOutputMsg:
            PrintOut = f"Solution: {self.mFinalOutputMsg}\n\n"
            AllKey = "Key: " + self.mSearchParams.mAllKeys + "\n"
            PathCost = f"Path Cost: {self.mSearchParams.mPathCost}\n\n"
            SearchParamStr = self.mSearchParams.PrintOutMetrics()
            DebugMsg = "First few expanded states:\n"
            if aDebug == "y":
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
            PrintOut = f"No solution found.\n\n"
            SearchParamStr = self.mSearchParams.PrintOutMetrics()
            # DebugMsg = "First few expanded states:\n"
            # if aDebug == "y":
            #     if (len(self.mPossibleMsg) < self.mDebugMsgsLen):
            #         for i in range(len(self.mPossibleMsg)):
            #             if i < len(self.mPossibleMsg)-1:
            #                 DebugMsg += self.mPossibleMsg[i] + "\n\n"
                            
            #             else:
            #                 DebugMsg += self.mPossibleMsg[i]
                    
            #     else:
            #         for i in range(self.mDebugMsgsLen):
            #             if i < self.mDebugMsgsLen-1:
            #                 DebugMsg += self.mPossibleMsg[i] + "\n\n"
                            
            #             else:
            #                 DebugMsg += self.mPossibleMsg[i]
            
            FinalOutput = PrintOut + SearchParamStr
        
        #----------------------------------------------------------------------
        return FinalOutput
                    
 
def task4(aAlgo, aMsgFile, aDictFile, aThresh,aLetters, aDebug):
    MsgEncoderObj = CMessageCoder()
    m = MsgEncoderObj.BlindSearch(aAlgo, aMsgFile, aDictFile, aThresh, aLetters, aDebug)

    return m
    
if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task4 function
    #print(task4('d', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    print(task4('b', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    #print(task4('i', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))        
            



