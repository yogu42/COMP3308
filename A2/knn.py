import csv
import numpy as np
import pandas as pd

def euclidean_distance(df, target):
    """
    Calculates the Euclidean distance between each row of a DataFrame and a target list.
    """
    
    # Ensure target is a numpy array
    target = np.array(target)

    # Calculate squared differences between each row and the target
    squared_diffs = np.sum((df - target)**2, axis=1)

    # Return the square root of the squared differences (Euclidean distance)
    return np.sqrt(squared_diffs)


def classify_nn(training_filename, testing_filename, k):
    df = pd.read_csv(training_filename, header=None) #training data
    test_data = pd.read_csv(testing_filename, header=None)
    df_except_last = df.iloc[:, :-1]
    output = []
    for i, row in test_data.iterrows():
        
      
      D = euclidean_distance(df_except_last, row)

      # adding a column of euclidean distances 
      df["D"] = D

      # obtain the second last column which shows the outcome
      
      k_smallest = df.nsmallest(k, 'D').iloc[:,-2]
      
      
      #selects the most frequent value
      o = k_smallest.value_counts()[:1].index[0]
      
      
      output.append(o)
    
    return output
classify_nn("pima.csv", "test.csv", 2)
