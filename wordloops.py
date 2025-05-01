import time, sys
elements = [
    # Letras minúsculas
    ' ','a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z',

    # Letras mayúsculas
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',

    # Números
    '0','1','2','3','4','5','6','7','8','9',

    # Símbolos comunes
    '!','@','#','$','%','^','&','*','(',')','-','_','=','+',
    '{','}','[',']','|','\\',':',';','"',"'",'<','>',',','.','?','/','`','~',

    # Espacio y otros
    ' '
]

word = input('Whats the word?:')

wordList=list(word)

ready = []

for i in wordList:
    for k in elements:
        new = ''.join(ready)
        if ready:
            try:
                if sys.argv[1]:
                    value = (f'/r{new}{k}',end='')
            except:
             
            else:
                value = f'{new}{k}'
            print(value)
            time.sleep(0.06)
        if k == i:
            ready.append(k)
            break
