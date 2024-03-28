# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:15:25 2024

@author: Thomas
"""
from Node import *

class CSearchToolParams:
    # Public class, all members accessible
    
    def __init__(self):
        # Algorithm flags
        self.mFlagDFS = "d"
        self.mFlagBFS = "b"
        self.mFlagUCS = "u"
        self.mFlagIDS = "i"
        
        # Some constants
        self.mLimit = 1000
        self.mYesLimit = 10

        # list of expanded and fringe
        self.mExpanded = []
        self.mFringe = []
        self.mCost = 0
        self.mExpandedNodes = 0
        self.mExpandedNodesVal = []
        
        # messages
        self.mNoSolution = "No solution found.\n\n"
        self.mKey = ""
    
    def Reset(self):
        # list of expanded and fringe
        self.mExpanded = []
        self.mFringe = []
        self.mCost = 0
        self.mExpandedNodes = 0
    
    def Add2Fringe(self,aNode):
        if isinstance(aNode, CNode):
            self.mFringe.append(CNode)
            
        else:
            raise TypeError("Must be a CNode Object type")
    
    def Add2Expanded(self,aNode):
        if isinstance(aNode, CNode):
            #self.mFringe.pop(CNode)
            self.mExpanded.append(CNode)
            self.mExpandedNodes += 1
            self.mExpandedNodesVal.append(CNode.GetValue())
        else:
            raise TypeError("Must be a CNode Object type")
    
    