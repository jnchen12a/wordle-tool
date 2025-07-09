from loguru import logger
from functools import total_ordering
from letterFrequencies import frequencies
from collections import Counter
import random
import copy

@total_ordering
class Word():
    def __init__(self, word: str) -> None:
        self.word = word
        self.score = 0
    
    def __eq__(self, other):
        return self.score == other.score
    
    def __lt__(self, other):
        return self.score < other.score
    
    def checkLetterInWord(self, l: str) -> bool:
        return l in self.word
    
    def checkLetterInWordPos(self, l: str, pos: int) -> bool:
        return self.word[pos] == l
    
    def getWord(self) -> str:
        return self.word

def readWordleFile(path='./wordle-list.txt') -> list:
    try:
        with open(path) as file:
            lines = file.readlines()
            lines = lines[1:-1]
    except:
        logger.error(f'ERROR: {path} is not valid.')
        exit(1)
    
    newList = []
    for i in range(len(lines)):
        newList.append(Word(''.join(c for c in lines[i] if c.isalpha())))

    newList = sorted(newList, reverse=True)
    return newList

def readWordBank(path='./words.txt') -> list:
    try:
        with open(path) as file:
            lines = file.readlines()
    except:
        logger.error(f'Error: {path} is not valid.')
        exit(1)

    res = [Word(''.join(c for c in line if c.isalpha())) for line in lines]
    res = sorted(res, reverse=True)
    
    return res

def checkYellow(posString: str, words: list) -> list:
    res = []
    positions = dict()
    for i, s in enumerate(posString):
        if s != '-':
            positions[i] = s

    onlyLetters = posString.replace('-', '')
    
    for word in words:
        add = True
        # reduce words to ones that have the letters
        for letter in onlyLetters:
            if not word.checkLetterInWord(letter):
                add = False
                break
        if not add:
            continue

        # remove the ones that have them in the yellow positions
        for i, letter in positions.items():
            if word.checkLetterInWordPos(letter, i):
                add = False
                break
        
        if add:
            res.append(word)
    
    return res

def getYellow() -> str:
    ipt = input('Type the letters (seperated by -) that appear in the word: ')
    ipt = ipt.lower()
    if len(ipt) != 5:
        logger.error('Error: Length of input must be 5.')
        exit(1)
    for l in ipt:
        if l != '-' and not l.isalpha():
            logger.error('Error: input characters must be - or a letter.')
            exit(1)
    return ipt

def getGray(ipt: str) -> list:
    l = [c for c in ipt]
    for letter in l:
        if not letter.isalpha():
            logger.error('Error: input characters must be a letter.')
            exit(1)
    return l

def getGreen() -> str:
    ipt = input('Type the position of the letters (with - for unknown) that appear in the word: ')
    ipt = ipt.lower()
    if len(ipt) != 5:
        logger.error('Error: Length of input must be 5.')
        exit(1)
    for l in ipt:
        if l != '-' and not l.isalpha():
            logger.error('Error: input characters must be - or a letter')
            exit(1)
    return ipt

def getYellowGreen(posString: str) -> tuple:
    yellowStr, greenStr, letters = '', '', ''
    for c in posString:
        if c == '-':
            greenStr += '-'
            yellowStr += '-'
        elif c.isupper():
            greenStr += c.lower()
            yellowStr += '-'
            letters += c.lower()
        else:
            greenStr += '-'
            yellowStr += c
            letters += c
    
    return yellowStr, greenStr, letters

def printWordListRandom(words: list) -> None:
    end = '...\n' if len(words) > 10 else '\n'
    print(f'({len(words)}): ', end='')
    if len(words) > 10:
        l = random.sample(words, 10)
    else:
        l = words
    for i, word in enumerate(l):
        # last one
        if i == (len(l) - 1) or i == 10:
            print(word.getWord(), end=end)
            break
        else:
            print(word.getWord(), end=', ')
    print('\033[0m', end='')

def printWordListOrder(words: list) -> None:
    end = '...\n' if len(words) > 10 else '\n'
    for i, word in enumerate(words):
        # last one
        if i == (len(words) - 1) or i == 10:
            print(word.getWord(), f'({word.score:.3f})', end=end)
            break
        else:
            print(word.getWord(), f'({word.score:.3f})', end=', ')
    print('\033[0m', end='')

def checkGreen(posString: str, words: list) -> tuple:
    res = []
    positions = dict()
    for i, s in enumerate(posString):
        if s != '-':
            positions[i] = s
    
    for word in words:
        add = True
        for pos, letter in positions.items():
            if not word.checkLetterInWordPos(letter, pos):
                add = False
                break
        if add:
            res.append(word)

    return res, list(positions.keys())

def checkGray(letters: list, words: list) -> list:
    res = []
    for word in words:
        add = True
        for letter in letters:
            if word.checkLetterInWord(letter):
                add = False
                break
        
        if add:
            res.append(word)
    
    return res

def printBonusWords(words: list, wordBank: list, greenPositions: list) -> list:
    # words is list of words it could be
    # allWords is entire word pool
    # guessed is all the letters we've already guessed
    pool = Counter()
    for word in words:
        w = word.getWord()
        pool.update(w)
    total = sum(pool.values())
    relativeFrequency = {k: (v / total) for k, v in pool.items()}
    # s is remaining pool of letters in all possible words, ignore the greenPositions
    s = set()
    for word in words:
        actualWord = word.getWord()
        for i in range(len(actualWord)):
            if i not in greenPositions:
                s.update(actualWord[i])

    bonusWords = []
    tempWordBank = copy.deepcopy(wordBank)
    for word in tempWordBank:
        w = set(word.getWord())
        score = 0
        for letter in s & w:
            score += relativeFrequency[letter]

        word.score = score
        bonusWords.append(word)

    
    bonusWords = sorted(bonusWords, reverse=True)
    if len(bonusWords) != 0:
        print('\033[33mWords that might be good guesses: ')
        printWordListOrder(bonusWords)

    return bonusWords

if __name__ == '__main__':
    allWords = readWordleFile()
    wordBank = readWordBank()

    print('Welcome to the Wordle Solver!')
    print(f'Number of words in word bank: {len(allWords)}')
    wordBank = printBonusWords(allWords, wordBank, [])

    words = allWords[:]
    newWordBank = wordBank[:]
    acceptedChars = set('12-')
    prevPoolSize = len(allWords)
    greenPositions = []
    while True:
        print('1. New game')
        print('2. Exit tool')
        c = input('Enter clues: ')
        if len(c) > 5:
            logger.error('ERROR: Input should be at most 5 characters long.')
            logger.error(f'ERROR: Input is actually {len(c)} characters long.')
            continue
        good = True
        for char in c:
            if (not char.isalpha()) and (char not in acceptedChars):
                logger.error(f'ERROR: {char} is not accepted here.')
                good = False
                break
        if not good:
            continue
        if c == '1':
            words = allWords[:]
            newWordBank = wordBank[:]
            prevPoolSize = len(allWords)
            greenPositions = []
            print('\033[31mNew game started!')
            print('\033[33mSuggested first words: ')
            printWordListOrder(wordBank)
            continue
        elif c == '2':
            print('Thank you for using the Wordle Tool!')
            break
        if '-' in c:
            print('\033[34mYellow Green detected.\033[0m')
            yellowStr, greenStr, letters = getYellowGreen(c)
            words = checkYellow(yellowStr, words)
            words, greenPositions = checkGreen(greenStr, words)
        else:
            print('\033[34mGray detected.\033[0m')
            letters = getGray(c)
            words = checkGray(letters, words)

        print(f'\033[32mPossible words: (reduced pool by {100 - ((len(words) / prevPoolSize) * 100):.2f}%)')
        prevPoolSize = len(words)
        printWordListRandom(words)
        if len(words) <= 2:
            print('\033[31mWordle has been solved!')
            print('New game started!\033[0m')
            words = allWords[:]
            newWordBank = wordBank[:]
            prevPoolSize = len(allWords)
            greenPositions = []
            print('\033[33mSuggested first words: ')
            printWordListOrder(wordBank)
        elif len(words) != 2:
            printBonusWords(words, wordBank, greenPositions)
