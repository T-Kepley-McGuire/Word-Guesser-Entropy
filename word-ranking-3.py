import re

import math

from typing import List, Tuple, Dict

def getPattern(guess: str, wordToGuess: str) -> str:
    pattern = ""
    for index, letter in enumerate(guess):
        if letter == wordToGuess[index]:
            pattern += "2"
        elif letter in wordToGuess:
            pattern += "1"
        else:
            pattern += "0"
    return pattern

def cullWordList(wordList: List[str], guess: str, pattern: str, log: bool = False) -> List[str]:
    if len(pattern) != 5 or len(guess) != 5:
        return print("error")
    
    posString = negString = posMaybeString = negMaybeString = ""

    for loc, curr in enumerate(pattern):
        negString += guess[loc] if curr == "0" else ""
        posMaybeString += f"(?=.*{guess[loc]})" if curr == "1" else ""
        negMaybeString += f"[^{guess[loc]}]" if curr == "1" else "."
        posString += guess[loc] if curr == "2" else "."

    posRegex = re.compile(f"^{posString.lower()}$")
    negRegex = re.compile(f"^[^{negString.lower()}]{{5}}$" if len(negString) > 0 else "")
    posMaybeRegex = re.compile(f"^{posMaybeString.lower()}.*$")
    negMaybeRegex = re.compile(f"^{negMaybeString.lower()}$")

    if log:
        print(f"word: {guess}, {pattern}\npositives: {posString}, {posRegex}\nnegatives: {negString}, {negRegex}\nmaybe so: {posMaybeString}, {posMaybeRegex}\nmaybe not: {negMaybeString}, {negMaybeRegex}\n")

    return [word for word in wordList if
            posRegex.match(word) and negRegex.match(word) and posMaybeRegex.match(word) and negMaybeRegex.match(word)]


def calculateAllEntropies(wordList: List[str]) -> List[Tuple[str, float]]:
    wordPatternsAsDictionaries: List[Dict[str, int]] = [{} for _ in range(len(wordList))]

    # for every possible guess...
    for index, guess in enumerate(wordList):
        # compare it to every possible answer
        # this second wordList can be replaced with any subset of possible guesses
        for goal in wordList:
            # with each comparison, get the pattern...
            pattern = getPattern(guess, goal)
            wordPatternsAsDictionaries[index][pattern] = wordPatternsAsDictionaries[index].get(pattern, 0) + 1
    
    def calcEntrop(wordPatterns: Dict[str, int]) -> float:
        def safeLog2(x: float) -> float:
            return math.log2(x) if x > 0 else 0
        entropy_sum = 0
        for pattern in wordPatterns:
            prob = wordPatterns[pattern] / len(wordList)
            entropy_sum += prob * safeLog2(1 / prob)
        return entropy_sum
    
    dictOfEntropy: Dict[str, float] = {}
    for index, wordPattern in enumerate(wordPatternsAsDictionaries):
        dictOfEntropy[wordList[index]] = calcEntrop(wordPattern)

    return sorted(dictOfEntropy.items(), key=lambda x: x[1], reverse=True)



def oOf2():

    f = open("words.txt")
        
    s = open("sorted-words-with-scores-3.txt", "w")

    wordList = []
    
    for line in f:
        wordList.append(line.strip())

    first = cullWordList(wordList, "tares", "02000")
    second = cullWordList(first, "magic", "02001", True)
    third = cullWordList(second, "candy", "12100", True)
    print(third)
    # sortedArrayOfEntropy = calculateAllEntropies(wordList)

    # s.writelines([f"{word[0]}: {word[1]:.3f}\n" for word in sortedArrayOfEntropy])


    f.close()
    s.close()

oOf2()