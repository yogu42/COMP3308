# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 18:32:48 2024

@author: Thomas
"""

class CNode:
    def __init__(self, aValue):
        self.mVal = aValue
        self.mCost= 1
        self.mDepth = 0
        
        self.mNumChild = 0
        self.mChildNodes = []
        self.mState = ""
        self.mParent = None
    
    def InsertNode(self,aChildNode):
        if isinstance(aChildNode,CNode):
            aChildNode.mDepth = self.mDepth + 1
            self.mChildNodes.append(aChildNode)
            self.mNumChild = len(self.mChildNodes)
    
    def GetValue(self):
        return self.mVal
    
    def AssignState(self,aNewState):
        self.mState = aNewState
        
    def GetCurrentState(self,aState):
        msg = list(aState) 
        for i in range(len(msg)):
            if msg[i] == self.mVal[0].lower():
                msg[i] = self.mVal[1].lower()
                                
            elif msg[i] == self.mVal[0]:
                msg[i] = self.mVal[1]
                                
            elif msg[i] == self.mVal[1].lower():
                msg[i] = self.mVal[0].lower()
                                
            elif msg[i] == self.mVal[1]:
                msg[i] = self.mVal[0]
                    
            self.mState = "".join(msg)
                
    
    def BackTrack(self):
        # Back track to find keys
        ParentNodesStr = []
        CurrentNode = self
        
        while CurrentNode:
            ParentNodesStr.append(CurrentNode.mVal)
            CurrentNode = CurrentNode.mParent
        
        ParentNodesStr.reverse()
        
        return ParentNodesStr

class CTree:
    def __init__(self):
        self.mRoot = CNode("  ")
        self.mRoot.mCost = 0
        self.mRoot.mDepth = 0
        
        self.mSwapPatterns = []
        self.mAllNodes = []
    
    def GetSwapPatterns(self,aPatterns):
        if not isinstance(aPatterns,list):
            raise TypeError("Wrong Type: Must be a list")

        self.mSwapPatterns = aPatterns
    
    def GenerateChildNodes(self,aParentNode):
        CurrentKey = aParentNode.GetValue()
        ChildNodeList = []
        
        for combo in self.mSwapPatterns:
            NewNode = CNode(combo)
            NewNode.mParent = aParentNode
            NewNode.mState = aParentNode.mState
            NewNode.GetCurrentState(aParentNode.mState)
            
            # Add child node
            aParentNode.InsertNode(NewNode)
            
            ChildNodeList.append(NewNode)
            
            self.mAllNodes.append(NewNode)
            

        #-------------------------------------------------
        return ChildNodeList
    
    def ReturnRoot(self):
        if isinstance(self.mRoot, CNode):
            return self.mRoot
