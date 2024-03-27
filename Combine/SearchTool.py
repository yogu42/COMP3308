# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:15:25 2024

@author: Thomas
"""
from Node import *

class CSearchToolParams:
    def __init__(self):
        # Algorithm flags
        self.mFlagDFS = "d"
        self.mFlagBFS = "b"
        self.mFlagUCS = "u"
        self.mFlagIDS = "i"
        
        # Some constants
        self.mLimit = 1000
        self.mYesLimit = 10
        
        # tree
        self.mTree = None
        self.mRoot = None
        
        # list of expanded and fringe
        self.mExpanded = []
        self.mFringe = []
        self.mCost = 0
        self.mExpandedNodes = 0
        
        # messages
        self.mNoSolution = "No solution found.\n\n"
        self.mKey = ""
    
    def Reset(self):
        # tree
        self.mTree = None
        self.mRoot = None
        
        # list of expanded and fringe
        self.mExpanded = []
        self.mFringe = []
        self.mCost = 0
        self.mExpandedNodes = 0
    
        