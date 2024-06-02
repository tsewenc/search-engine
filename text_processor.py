from porter2stemmer import Porter2Stemmer
import hashlib
import math

def isAlpNum(chr: str) -> bool:
    #return true if the character is within the range of a-z A-Z or 0-9
    return ord('a') <= ord(chr) <= ord('z') or ord('0') <= ord(chr) <= ord('9') or ord('A') <= ord(chr) <= ord('Z')

def tokenize(text) -> {list, list}:
    porter2Stemmer1 = Porter2Stemmer() #declaring snowballStemmer object
    tokens = []
    stemmed_tokens = [] # Create a new list of stemmed tokens
    current_word = []
    for char in text:
        if isAlpNum(char):
        # if char.isalpha() or char.isdigit():
            current_word.append(char)
        elif len(current_word) != 0:
            word = "".join(current_word).lower()
            tokens.append(word)
            stemmed_tokens.append(porter2Stemmer1.stem(word)) # appending stemmed tokens
            current_word = []
    if current_word:
        word = "".join(current_word).lower()
        tokens.append(word)
    return tokens, stemmed_tokens

def get_word_freq(tokens):
    word_freq_dict = {}
    for token in tokens:
        if token[0] not in word_freq_dict:
            word_freq_dict[token[0]] = [0, 0]
        word_freq_dict[token[0]][0] += 1
        if token[1]:
            word_freq_dict[token[0]][1] = 1

    sqr_sum = 0
    for token, info in word_freq_dict.items():
        word_freq_dict[token] = [(1 + math.log(info[0])) * info[1], info[0]]
        sqr_sum += word_freq_dict[token][0] ** 2

    stand_div = math.sqrt(sqr_sum)

    for token, info in word_freq_dict.items():
        word_freq_dict[token] = [info[0] / stand_div, info[0], info[1]]
    return word_freq_dict

def simhash(tokens, hash_bits=128):
    tokens = {t: i[2] for t, i in tokens.items()}
    V = [0] * hash_bits
    for word, count in tokens.items():
        hash_value = int(hashlib.md5(word.encode('utf-8')).hexdigest(), 16)
        for i in range(hash_bits):
            # extracts the value of the i-th bit from the right of hash_value
            bit = (hash_value >> i) & 1
            if bit == 1:
                V[i] += count
            else:
                V[i] -= count
    fingerprint = 0
    for i in range(hash_bits):
        if V[i] >= 0:
            # sets the i-th bit of fingerprint to 1 without affecting the other bits
            fingerprint |= (1 << i)
    return fingerprint

def are_similar(fingerprint_a, fingerprint_b, threshold, hash_bits=128):
    # XOR to find differing bits
    differing_bits = fingerprint_a ^ fingerprint_b

    # Count the number of same bits
    same_bits = hash_bits - bin(differing_bits).count('1')

    # Calculate similarity as the fraction of bits that are the same
    similarity = same_bits / hash_bits
    return similarity >= threshold

def is_new_fingerprint(new_fingerprint, fingerprints):
    for value in fingerprints:
        if are_similar(new_fingerprint, value, 0.93):
            return False
    return True

if __name__ == "__main__":
    pass