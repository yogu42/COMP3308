import numpy as np
import pandas as pd

def pdf(x, mu, sigma):  # Example for normal distribution
  """
  Calculates the probability density function (PDF) for a specific distribution.

  Args:
      x: A numerical value for which to calculate the PDF.
      mu: Mean of the distribution.
      sigma: Standard deviation of the distribution.

  Returns:
      The PDF value at the given x.
  """

  

  # Example for normal distribution:
  return (1 / (sigma * np.sqrt(2*np.pi))) * np.exp((-((x - mu)**2) / (2 * sigma**2)))

  

def classify_nb(training_filename, testing_filename):
  
    df = pd.read_csv(training_filename, header=None) #training data
    test_data = pd.read_csv(testing_filename, header=None)
    df_except_last = df.iloc[:, :-1]
    output = []
    
    yes = df.iloc[:,-1]=="yes" #no headers, selecting all rows (:) against last col
    no = df.iloc[:,-1]=="no"
    
    df_yes = df[yes].iloc[:, :-1] #excluding last column
    df_no = df[no].iloc[:, :-1] 
    
    p_yes = len(df_yes) / len(df)
    p_no = len(df_no) / len(df)

    for i, row in test_data.iterrows():
        j = 0
        p_E_yes = 1
        p_E_no = 1
        for series_name, series in df_yes.items():
            x = row[j]
            mean = series.mean()
            std = series.std()
            pdf_value = pdf(x, mean, std)
            p_E_yes *= pdf_value
            j += 1

        p_yes_E = p_E_yes * p_yes

        k = 0
        for series_name, series in df_no.items():
            x = row[k]
            mean = series.mean()
            std = series.std()
            pdf_value = pdf(x, mean, std)
            p_E_no *= pdf_value
            k += 1

        p_no_E = p_E_no * p_no

        if (p_yes_E >= p_no_E):
            output.append("yes")
        else:
            output.append("no")
    return output
  
  
  
  
 
classify_nb("pima.csv", "test.csv")