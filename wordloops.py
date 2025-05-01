elements = []

word = input('Whats the word?:')

wordList=list(word)

for i in wordList:
    for k in elements:
        print(k)
        if k == i:
            break
