def task1(key, filename, indicator):
    #TODO
    if indicator == 'e':
      swaps = [key[i:i+2] for i in range(0, len(key), 2)]
    elif indicator == 'd':
      swaps = [key[i:i+2] for i in range(0, len(key), 2)]
      swaps.reverse()
    #print(swaps)
    
    with open(filename, 'r') as file:
      contents = file.read()
    #print(contents)
    #MAKE SWAPS CONTINUOUS
    new_string = ""
    
    for char in contents:
      
      swapped = False
      letter = char
      for swap in swaps:
        
        if swap[1] == letter:
          #new_string += swap[0]
          letter = swap[0]
          swapped = True
          
        elif swap[1].lower() == letter:
          #new_string += swap[0].lower()
          letter = swap[0].lower()
          swapped = True
        elif swap[0] == letter:
          #new_string += swap[1]
          letter = swap[1]
          swapped = True
          
        elif swap[0].lower() == letter:
          #new_string += swap[1].lower()
          letter = swap[1].lower()
          swapped = True
          
      
      if not swapped:
        new_string += char
        
      else:
        new_string += letter
      
    return new_string

if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task1 function
    print(task1('AE', 'spain.txt', 'd'))
    print(task1('VFSC', 'ai.txt', 'd'))
    print(task1('ABBC', 'cabs_plain.txt', 'e'))
    