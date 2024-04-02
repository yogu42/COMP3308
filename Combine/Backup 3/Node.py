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
        self.mState = None
        self.mParent = None
    
    def InsertNode(self,aChildNode):
        if isinstance(aChildNode,CNode):
            aChildNode.mDepth = self.mDepth + 1
            self.mChildNodes.append(aChildNode)
            self.mNumChild = len(self.mChildNodes)
    
    def GetValue(self):
        return self.mVal

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
            aParentNode.InsertNode(NewNode)
            ChildNodeList.append(NewNode)
            self.mAllNodes.append(NewNode)

        #-------------------------------------------------
        return ChildNodeList
    
    def ReturnRoot(self):
        if isinstance(self.mRoot, CNode):
            return self.mRoot
