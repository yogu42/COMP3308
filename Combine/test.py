# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 20:17:51 2024

@author: Thomas
"""

C = "ABCDKL"

s = []
swap ={}
t = []
for c in range(len(C)-1):
    swap[C[c]] = []
    
for i in range(len(C)-1):
    for j in range(i+1, len(C)):
        if C[i] in swap:
            swap[C[i]].append(C[j])


for k in range(len(C)-1):
    for n in range (k + 1,len(C)):
        comb = C[k] + C[n]
        t.append(comb)


for key,val in swap.items():
    for l in val:
        node = key + l
        s.append(node)

if t == s:
    print(True)


# Generate combinations and construct graph

        
    