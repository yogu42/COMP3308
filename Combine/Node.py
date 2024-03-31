# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 18:32:48 2024

@author: Thomas
"""

class CNode:
    def __init__(self, aValue):
        self.mVal = aValue
        self.mCost= 1
        self.mNumChild = 0
        self.mChildNodes = []
    
    def InsertNode(self,aChildNode):
        if isinstance(aChildNode,CNode):
            self.mChildNodes.append(aChildNode)
            self.mNumChild = len(self.mChildNodes)
    
    def GetValue(self):
        return self.mVal

class CTree:
    def __init__(self):
        self.mRoot = CNode("  ")
        self.mRoot.mCost = 0
        
        self.mSwapPatterns = []
        self.mAllNodes = []
    
    def GetSwapPatterns(self,aPatterns):
        if not isinstance(aPatterns,list):
            raise TypeError("Wrong Type: Must be a list")
        
        else:
            for e in aPatterns:
                if not isinstance(e, dict):
                    raise TypeError("Wrong Type: Must be a dictionary with STR key and [] value")
        
        self.mSwapPatterns = aPatterns
    
    def GenerateChildNodes(self,aParentNode):
        CurrentKey = aParentNode.GetValue()
        ChildNodeList = []
        
        if CurrentKey == "  ":
            for combo in self.mSwapPatterns:
                for l1,l2 in combo.items():
                    for letter in l2:
                        NewNode = CNode(l1 + letter)
                    
                        ChildNodeList.append(NewNode)
                        aParentNode.InsertNode(NewNode)
        else:
            for combo in self.mSwapPatterns:
                for l1,l2 in combo.items():
                    if l1 == CurrentKey[0]:
                        # Find second letter index
                        ind = l2.index(CurrentKey[1])
                        for i in range(ind,len(l2)):
                            NewNode = CNode(l1 + l2[i])
                            ChildNodeList.append(NewNode)
                            aParentNode.InsertNode(NewNode)

        #-------------------------------------------------
        return ChildNodeList
    
    def ReturnRoot(self):
        if isinstance(self.mRoot, CNode):
            return self.mRoot
        
    def PrintTree(self):
        # Start from root and print it
        pass
        

            
            
            
                
        
        
        
        
        
        
        
            
    
    
        

