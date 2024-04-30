import numpy as np
import csv 

from dataclasses import dataclass

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
        

class DataProcessor:
    def __init__(self):
        """Class extracts and stores data from csv file"""
        self.file_name = None
        self.data_extracted = False
        self.data_processed = False
        
        self.header_index = {}
        self.raw_data = []
        self.processed_data = {}
        self.normalise_data = {}
        
    def ReadCsv(self,csv_dir):
        assert isinstance(csv_dir, str), "Input directory must be a string"
        
        try:
            self.file_name = csv_dir
            
            with open(csv_dir, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Read the header
                
                # set up data dictionary and indices that corresponds
                for h in header:
                    self.header_index[header.index(h)] = h
                    self.processed_data[h] = []
                
                # read all raw data s
                self.raw_data = list(reader)  # Read the rest of the data
                
                for data_row in self.raw_data:
                    for data in data_row:
                        #Check if data is a float,, int or str
                        data_conv = Convert2Data(data)
                        
                        # Using data, gets its index from the data row to get
                        # the key from the header index dictionary
                        data_ind = data_row.index(data)
                        key = self.header_index[data_ind]
                        
                        self.processed_data[key].append(data_conv)
            
            self.data_extracted = True
            print("CSV file successfully read")

        
        except FileNotFoundError:
            print("CSV file raed failed")
        
        
        def NormaliseData(self,file_name):
            assert self.data_extracted is True, "data have not been extracted"
            
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                
                # Write header
                writer.writerow(self.processed_data.keys())
                
                # Transpose data to write by row
                rows = zip(*self.processed_data.values())
                
                # Write rows
                writer.writerows(rows)
                
            print("Data successfully written to CSV file:", file_name)
            
        
        def Output2CSV(self,file_name):
            """
            Class method transfer all processed data back into csv file
        
            """
            pass 
            

Extractor = DataProcessor()
Extractor.ReadCsv("occupancy_org.csv")

