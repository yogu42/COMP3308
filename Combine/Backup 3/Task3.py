import string

def task3(message_filename, dictionary_filename, threshold):
    #TODO
    
    with open(message_filename, 'r') as file:
      contents = file.read()
    
    dictionary = []
    with open(dictionary_filename, 'r') as file:
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
    
    valid = True if percentage >= threshold else False
    
    r = str(valid) + "\n" + f"{percentage:.2f}"
    return r

if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task3 function
    print(task3('jingle_bells.txt', 'dict_xmas.txt', 90))
    print(task3('fruit_ode.txt', 'dict_fruit.txt', 80))
    #print(task3('amazing_poetry.txt', 'common_words.txt', 95))
    