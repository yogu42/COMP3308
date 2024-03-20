import itertools
def combine_in_order(letter1, letter2):
    # Check if the letters are in alphabetical order
    if letter1 > letter2:
        letter1, letter2 = letter2, letter1  # Swap them
    # Combine them back into a single string
    return letter1 + letter2


def task2(filename, letters):
    #TODO
    # Generate all 2-letter combinations of the input letters
    combinations = itertools.combinations(letters, 2)
    
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
    
    with open(filename, 'r') as file:
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

if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task2 function
    print(task2('spain.txt', 'ABE'))
    print(task2('ai.txt', 'XZ'))
    print(task2('cabs.txt', 'ABZD'))
    
 
    
    