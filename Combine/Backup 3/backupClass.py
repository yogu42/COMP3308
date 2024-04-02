
"""
Created on Sat Mar 23 13:40:43 2024

@author: Thomas
"""
import itertools
import string
class CMessageCoder:
    def __init__(self):
        self.mEncodeMode = "e"
        self.mDecodeMode = "d"
        
        self.mInputMsg = None
        self.mOutputMsg = ""

        # Algorithm flags
        self.flagDFS = "d"
        self.flagBFS = "b"
        self.flagUCS = "u"
        self.flagIDS = "i"
        
                
    def SecretMsg(self, aKey, aFilename, aMode):
        if aMode == self.mEncodeMode:
            swaps = [aKey[i:i+2] for i in range(0, len(aKey), 2)]
              
        elif aMode == self.mDecodeMode:
            swaps = [aKey[i:i+2] for i in range(0, len(aKey), 2)]
            swaps.reverse()
        else:
            raise TypeError("Wrong input")

        # Open file 
        with open(aFilename, 'r') as file:
            self.mInputMsg = file.read()
        
        # # iterate characters 
        for char in self.mInputMsg:
            swapped = False
            letter = char
            
            # Swap letters
            for swap in swaps:
                if swap[1] == letter:
                    letter = swap[0]
                    swapped = True
                  
                elif swap[1].lower() == letter:
                    letter = swap[0].lower()
                    swapped = True
                        
                elif swap[0] == letter:
                    letter = swap[1]
                    swapped = True
                  
                elif swap[0].lower() == letter:
                    letter = swap[1].lower()
                    swapped = True
            
            # Construct output message 
            if not swapped:
                self.mOutputMsg += char
                
            else:
                self.mOutputMsg += letter
                
        # Output message
        return self.mOutputMsg
    
    def SearchSpace (self, aFilename, aLetters):
        def combine_in_order(letter1, letter2):
            # Check if the letters are in alphabetical order
            if letter1 > letter2:
                letter1, letter2 = letter2, letter1  # Swap them
                # Combine them back into a single string
            return letter1 + letter2
        
        # Generate all 2-letter combinations of the input letters
        combinations = itertools.combinations(aLetters, 2)
        
        # Create a list to hold combinations as strings
        swaps2 = []
        for combo in combinations:
            swaps2.append(''.join(combo))# Convert tuple to string
            
        # List to store pairs in alphabetical order
        swaps = [] 
        for swap in swaps2:
            # Ensure each letter pair is in alphabetical order
            swaps.append(combine_in_order(swap[0], swap[1]))
        
        # Sort the swaps alphabetically
        swaps.sort()
        print(swaps)
        
        with open(aFilename, 'r') as file:
            contents = file.read()
        
        # List to store all possible strings after swap operations
        successor = []
        for swap in swaps:
            new_string = ""
            # Iterate through each character in the original content
            for char in contents:
                letter = char
                swapped = False
            
                # Check and perform the necessary letter swaps
                if swap[1] == letter:
                    letter = swap[0]
                    swapped = True
                    
                elif swap[1].lower() == letter:
                    letter = swap[0].lower()
                    swapped = True
                    
                elif swap[0] == letter:
                    letter = swap[1]
                    swapped = True
                    
                elif swap[0].lower() == letter:
                    letter = swap[1].lower()
                    swapped = True
          
                new_string += char if not swapped else letter
            
            # Add the new string to the successor list if it is different from the original
            if contents != new_string:
                successor.append(new_string)
        
        r = ""
        r += str(len(successor))
        if len(successor) != 0:
            r += "\n"
    
        for i, s in enumerate(successor):
            if i < len(successor) - 1:
                r += s
                r += "\n\n"
            else:
                r += s
        return r
    
    def Goal(self,aMsgFileName,aDirName,aThreshold ):
        #TODO
        with open(aMsgFileName, 'r') as file:
          contents = file.read()
        
        dictionary = []
        with open(aDirName, 'r') as file:
          for line in file:
            clean_line = line.rstrip()
            dictionary.append(clean_line)
        
        # Define all punctuation symbols you want to remove
        remove_symbols = string.punctuation  # Includes symbols like !, ?, ., and ,
    
        # Create a translation table. Third argument is the string of symbols to remove.
        trans_table = contents.maketrans('', '', remove_symbols)
    
        # Remove the symbols from the string
        clean_string = contents.translate(trans_table)
    
        word = clean_string.split()
        
        count = 0
        for w in word:
          for c in dictionary:
            if w.lower() == c.lower():
              count += 1
        
        percentage = round(count/len(word), 4) * 100
        
        valid = True if percentage >= aThreshold else False
        
        r = str(valid) + "\n" + f"{percentage:.2f}"
        return r
    
    def BlindSearch(self,aAlgo, aMsgFile, aDictFile, aThresh,aLetters, aDebug):
        pass
        
        

def task1(key, filename, indicator):
    MsgCoder = CMessageCoder()
    out = MsgCoder.SecretMsg(key, filename, indicator)
    return out

def task2(filename, letters):
    MsgCoder = CMessageCoder()
    out = MsgCoder.SearchSpace(filename, letters)
    return out

def task3(message_filename, dictionary_filename, threshold):
    MsgCoder = CMessageCoder()
    out = MsgCoder.Goal(message_filename, dictionary_filename, threshold)
    return out

def task4():
    pass

def task5():
    pass

def task6():
    pass



if __name__ == '__main__':
    # Task 1
    # print(task1('AE', 'spain.txt', 'd'))
    # print(task1('VFSC', 'ai.txt', 'd'))
    # print(task1('ABBC', 'cabs_plain.txt', 'e'))
    
    # Task 2
    print(task2('spain.txt', 'ABE'))
    print(task2('ai.txt', 'XZ'))
    print(task2('cabs.txt', 'ABZD'))
    
    # Task 3
    # print(task3('jingle_bells.txt', 'dict_xmas.txt', 90))
    # print(task3('fruit_ode.txt', 'dict_fruit.txt', 80))
    # print(task3('amazing_poetry.txt', 'common_words.txt', 95))
    
    # # print(task3('jingle_bells.txt', 'dict_xmas.txt', 90))
    # # print(task3('fruit_ode.txt', 'dict_fruit.txt', 80))
    # # print(task3('amazing_poetry.txt', 'common_words.txt', 95))
