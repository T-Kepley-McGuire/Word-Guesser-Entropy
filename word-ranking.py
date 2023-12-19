import re
import time

def getWordEvalListsFromGuesses(guess, wordToGuess):
    pos = ["", "", "", "", ""]
    neg = []
    may = ["", "", "", "", ""]

    
    for index, letter in enumerate(guess):
        if letter == wordToGuess[index]:
            pos[index] = letter
        elif letter in wordToGuess:
            may[index] = letter
        else:
            neg.append(letter)

    return pos, neg, may


def checkAgainstFoundInfo(wordList, positives, negatives, maybes):
    if len(positives) != 5:
        print("error")
    if len(maybes) != 5:
        print("error")

    posString = "".join(["." if curr == "" else curr for curr in positives])
    negString = "".join(negatives)
    posMaybesString = "".join([f"(?=.*{curr})" if curr != "" else "" for curr in maybes])
    negMaybesString = "".join(["." if curr == "" else f"[^{curr}]" for curr in maybes])

    posRegex = re.compile(f"^{posString.lower()}$")
    negRegex = re.compile(f"^[^{negString.lower()}]{{5}}$" if len(negString) > 0 else "")
    posMaybeRegex = re.compile(f"^{posMaybesString.lower()}.*$")
    negMaybeRegex = re.compile(f"^{negMaybesString.lower()}$")

    sum = 0
    for word in wordList:
        if posRegex.match(word) and negRegex.match(word) and posMaybeRegex.match(word) and negMaybeRegex.match(word):
            sum += 1

    return sum
    return [word for word in wordList if
            posRegex.match(word) and negRegex.match(word) and posMaybeRegex.match(word) and negMaybeRegex.match(word)]





def oOf3():
        
    f = open("words.txt")
        
    w = open("words-with-scores.txt", "w")
    s = open("sorted-words-with-scores.txt", "w")

        
    wordList = []
    wordRanks = []

    for line in f:
        wordRanks.append({"word": line.strip(), "score": 0})
        wordList.append(line.strip())
    f.close()

    print(f"Finished reading file. Beginning ranking with {len(wordRanks)} words. ")
    for index, wordObject in enumerate(wordRanks):
        for goal in wordList:
            pos, neg, may = getWordEvalListsFromGuesses(wordObject["word"], goal)
            lenFilteredList = checkAgainstFoundInfo(wordList, pos, neg, may)
            wordObject["score"] += lenFilteredList
        wordObject["score"] /= (0.0 + len(wordRanks))
        text = str(wordObject["word"]) + " " + str(round((wordObject["score"] + 0.0), 2)) + "\n"
        w.write(text)
        if round((index - 1.0)/len(wordRanks), 3) != round((index - 0.0) / len(wordRanks), 3):
            print(f"{round((index) / len(wordRanks), 2) * 100}% done")


    w.close()

    print("Finished calculating scores. Sorting and writing to file")

    wordRanks.sort(key=lambda x: x["score"], reverse=True)
    s.writelines([f"{wordObject['word']} {round(wordObject['score'] + 0.0, 2)}\n" for wordObject in wordRanks])
    s.close()





start = time.time()
oOf3()
end = time.time()
print(f"||| Elapsed Time: {round(end - start, 3)} seconds")
# pos, neg, may = getWordEvalListsFromGuesses(["agree", "boner", "cried", "trues"], "trees")

# filteredList = checkAgainstFoundInfo(wordList, pos, neg, may)

