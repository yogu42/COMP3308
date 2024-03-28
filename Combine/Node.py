# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 18:32:48 2024

@author: Thomas
"""

class CNode:
    def __init__(self, aValue,):
        self.mVal = aValue
        self.mCost= 1
        self.mLeftChild = None
        self.mRightChild = None
    
    def InsertLeftNode(self,aChildNode):
        if isinstance(aChildNode,CNode):
            self.mLeftChild = aChildNode
    
    def InsertRightNode(self,aChildNode):
        if isinstance(aChildNode,CNode):
            self.mRightChild = aChildNode
    
    def GetValue(self):
        return self.mVal

class CTree:
    def __init__(self):
        self.mRoot = None
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
    
    def GenerateStructure(self):
        # Use tuple of swap patterns to create.
        # A:B,C,D,E
        # B:C,D,E
        # C:D,E
        # D:E
        # ...
        # Each line represents a branch with the key of the dict being first
        # letter and the second being the letter it is swapping for. Combine
        # both u have a node. 
        # The line following represent other branch but its first combo is the
        # right child node of the first node of the first branch and so on
        #                   AB
        #                  /  \
        #                 AC   BC
        #                /    /  \
        #               AD   BD  CD
        #              /    /   /  \
        #             AE   BE  CE  DE
        # Create all swap combos
        for pattern in self.mSwapPatterns:
            newBranch = []
            for key,swaps in pattern.items():
                for letter in swaps:
                    newNode = CNode(key + letter)
                    newBranch.append(newNode)
            
            self.mAllNodes.append(newBranch)
            
        # Iterate the allNode list and link the nodes
        # First letter of child node matches first letter of parent node,
        # it is on the Left of the Parent Node
        
        # Second letter of child node matches second letter of parent node,
        # it is on the RIGHT of the Parent Node
        
        # Establish the branches
        for branch in self.mAllNodes:
            for l in range(1,len(branch)):
                branch[l-1].InsertLeftNode(branch[l])
            
        for i in range(len(self.mAllNodes)-1):
            self.mAllNodes[i][0].InsertRightNode(self.mAllNodes[i+1][0])
        
        self.mRoot = self.mAllNodes[0][0]
    
    def ReturnRoot(self):
        if isinstance(self.mRoot, CNode):
            return self.mRoot
        
    def PrintTree(self):
        # Start from root and print it
        pass
        


            

            
            
            
                
        
        
        
        
        
        
        
            
    
    
        

