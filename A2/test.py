# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 16:46:48 2024

@author: Thomas
"""

def Convert2Data(input_data):
    '''
    Take in string, check if its a float or int then return it
    '''
    # Convert to str, int or float depending on input
    length = len(input_data)
    is_dot = '.' in input_data 
    num_count = 0
    
    conv = input_data
    # check i its a float
    if is_dot:
        for c in input_data:
            if c.isdigit():
                num_count += 1
        
        if num_count == (length - 1):
            conv = float(input_data)
            
    else:
        for c in input_data:
            if c.isdigit():
                num_count += 1
        
        if num_count == length:
            conv = int(input_data)
        
    return conv
        
c = Convert2Data("12")
