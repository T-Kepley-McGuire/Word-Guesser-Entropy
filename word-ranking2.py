import time

def calculate_word_frequencies(word_list):
    word_frequencies = {}
    for word in word_list:
        for letter in word:
            if letter in word_frequencies:
                word_frequencies[letter] += 1
            else:
                word_frequencies[letter] = 1
    return word_frequencies


def calculate_word_signatures(word_list, word_frequencies):
    word_signatures = {}
    for word in word_list:
        signature = {letter: word_frequencies[letter] for letter in word}
        word_signatures[word] = signature
    return word_signatures


def calculate_guess_signature(guess, word_frequencies):
    guess_signature = {letter: word_frequencies[letter] if letter in word_frequencies else 0 for letter in guess}
    return guess_signature


def eliminate_words(word_signatures, guess_signature):
    eliminated_words = [word for word, signature in word_signatures.items() if any(signature[letter] != guess_signature[letter] for letter in signature)]
    return eliminated_words


def chatGPT():
    # Read words from file
    word_list = [line.strip() for line in open("words.txt")]

    # Step 1: Calculate letter frequencies
    word_frequencies = calculate_word_frequencies(word_list)

    # Step 2: Calculate word signatures
    word_signatures = calculate_word_signatures(word_list, word_frequencies)
    print(word_signatures)

    # Step 3: Calculate guess signature
    guess = "night"  # Replace with the actual guess
    guess_signature = calculate_guess_signature(guess, word_frequencies)
    print(guess_signature)

    # Step 4: Eliminate words based on signatures
    eliminated_words = eliminate_words(word_signatures, guess_signature)

    # Step 5: Update scores
    score = len(word_list) - len(eliminated_words)

    print(f"Score for '{guess}': {score}")


start = time.time()
chatGPT()
end = time.time()
print(f"||| Elapsed Time: {round(end - start, 3)} seconds")