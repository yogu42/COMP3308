def task1(key, filename, indicator):
    #TODO
    if indicator == 'e':
        swaps = [key[i:i+2] for i in range(0, len(key), 2)]
    elif indicator == 'd':
        swaps = [key[i:i+2] for i in range(0, len(key), 2)]
        swaps.reverse()
    
    with open(filename, 'r') as file:
      contents = file.read()
    #print(contents)
    #MAKE SWAPS CONTINUOUS
    
    StrList = list(contents)
    
    for swap in swaps:
        for i in range(len(StrList)):
            if StrList[i] == swap[0].lower():
                StrList[i] = swap[1].lower()
                    
            elif StrList[i] == swap[0]:
                StrList[i] = swap[1]
                    
            elif StrList[i] == swap[1].lower():
                StrList[i] = swap[0].lower()
                    
            elif StrList[i] == swap[1]:
                StrList[i] = swap[0]

    
    new_string = ''.join(StrList)

        
        
    return new_string

if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task1 function
    print(task1('AE', 'spain.txt', 'd'))
    print(task1('VFSC', 'ai.txt', 'd'))
    print(task1('ABBC', 'cabs_plain.txt', 'e'))
    