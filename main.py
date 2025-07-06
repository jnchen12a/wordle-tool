from loguru import logger
from functools import total_ordering
from letterFrequencies import frequencies
from collections import Counter
import random

@total_ordering
class Word():
    def __init__(self, word: str) -> None:
        self.word = word
        self.calculateScore(set())
    
    def calculateScore(self, guessed: set) -> None:
        s = set(self.word)
        vowels = set('aeiou')
        score = 0
        for letter in s:
            if letter in guessed:
                continue
            if letter in vowels:
                score += 2
            else:
                score += 1
            score += frequencies[letter] * 0.001
        self.score = score
    
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

def readWordleFile(path='./wordle-list') -> list:
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
    print(f'({len(words)}): ', end='')
    for i, word in enumerate(words):
        # last one
        if i == (len(words) - 1) or i == 10:
            print(word.getWord(), end=end)
            break
        else:
            print(word.getWord(), end=', ')
    print('\033[0m', end='')

def checkGreen(posString: str, words: list) -> list:
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

    return res

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

def recalculateScores(words: list, guessed: set) -> list:
    for word in words:
        word.calculateScore(guessed)

    return sorted(words, reverse=True)

def printBonusWords(words: list, wordBank: list, guessed: set) -> None:
    # words is list of words it could be
    # allWords is entire word pool
    # guessed is all the letters we've already guessed
    pool = Counter()
    for word in words:
        w = word.getWord()
        pool.update(w)
    # s is remaining pool of letters in all possible words
    s = set()
    for word in words:
        s.update(word.getWord())

    bonusWords = []
    tempWordBank = wordBank[:]
    for word in tempWordBank:
        w = set(word.getWord())
        score = len(s & w)
        score -= len(w & guessed)

        if score > 3:
            word.score = score
            bonusWords.append(word)

    
    bonusWords = sorted(bonusWords, reverse=True)
    if len(bonusWords) != 0:
        print('\033[33mOther words that might be good guesses: ')
        printWordListOrder(bonusWords)

def shortenWordBank(newWordBank: list, goodWords: list) -> list:
    res = []
    for word in goodWords:
        add = True
        for bankWord in newWordBank:
            if word.getWord() == bankWord.getWord():
                add = False
                break
        
        if add:
            res.append(word)

    return res

if __name__ == '__main__':
    allWords = readWordleFile()
    wordBank = readWordBank()

    print('Welcome to the Wordle Solver!')
    print('\033[33mSuggested first words: ')
    printWordListOrder(wordBank)

    words = allWords[:]
    newWordBank = wordBank
    guessed = set()
    acceptedChars = set('12-')
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
            guessed = set()
            newWordBank = wordBank
            print('New game started!')
            print('\033[33mOSuggested first words: ')
            printWordListOrder(newWordBank)
            continue
        elif c == '2':
            print('Thank you for using the Wordle Tool!')
            break
        elif '-' in c:
            print('\033[34mYellow Green detected.\033[0m')
            yellowStr, greenStr, letters = getYellowGreen(c)
            words = checkYellow(yellowStr, words)
            words = checkGreen(greenStr, words)
            newWordBank = shortenWordBank(newWordBank, words)
            for letter in letters:
                guessed.add(letter)
            words = recalculateScores(words, guessed)
        elif '' != c:
            print('\033[34mGray detected.\033[0m')
            letters = getGray(c)
            words = checkGray(letters, words)
            newWordBank = shortenWordBank(newWordBank, words)
            for letter in letters:
                guessed.add(letter)
            words = recalculateScores(words, guessed)

        print('\033[32mPossible words:')
        printWordListRandom(words)
        if len(words) == 1:
            print('Wordle has been solved!')
            print('New game started!')
            words = allWords[:]
            guessed = set()
            newWordBank = wordBank
            print('\033[33mOSuggested first words: ')
            printWordListOrder(newWordBank)
        elif len(words) != 2:
            printBonusWords(words, newWordBank, guessed)
