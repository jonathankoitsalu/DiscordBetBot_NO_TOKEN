def LetterToEmoji(letter):
    letterDict = {'A' : '🇦', 
        'B' : '🇧', 
        'C' : '🇨', 
        'D' : '🇩', 
        'E' : '🇪', 
        'F' : '🇫', 
        'G' : '🇬', 
        'H' : '🇭', 
        'I' : '🇮'}
    return letterDict[letter]

def letterEmoji(number):
    letterEmojis = ['🇦', 
        '🇧', 
        '🇨', 
        '🇩', 
        '🇪', 
        '🇫', 
        '🇬', 
        '🇭', 
        '🇮']
    return letterEmojis[number]
