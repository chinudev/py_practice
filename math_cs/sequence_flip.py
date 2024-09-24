

def follow_sequence(word, sequence):
    wordList = list(word)
    for (i, j) in sequence:
        wordList[i], wordList[j] = wordList[j], wordList[i] 
    return ''.join(wordList)

#seq = [( 0,1 ), (1,3),(4,5)]  # marine -> airmen
seq = [( 0,1 ), (2,3), (1,2),(2,3), (4,5)]  # marine -> airmen
print(follow_sequence('marine', seq))
