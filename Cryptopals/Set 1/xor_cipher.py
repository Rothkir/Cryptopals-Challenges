import fixed_xor as fx
from string import ascii_lowercase, ascii_uppercase
from collections import Counter
import sys

impossible_chars = set([
    '\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\x0b', '\x0c', '\x0e',
    '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19',
    '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f', '\x7f'
])
letters_and_space = set(" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
punctuation = set(".,!?'-\n")


def frequency_analysis(cipher):
    # Counts all chars in text
    normal_symbols = "0123456789 .,!?'-\n"

    allowed = set(ascii_lowercase + ascii_uppercase + normal_symbols + ''.join(impossible_chars))

    char_counts = Counter(c for c in cipher if c in allowed)
    total_letters = sum(char_counts.values())
    
    if total_letters == 0:
        return {}

    # This is the list holding all the frequencies. Stored in alphabetical order 
    chars_frequency = {
        letter: (char_counts[letter] / total_letters) * 100
        for letter in allowed
    }

    chars_frequency = dict(sorted(chars_frequency.items(), key=lambda x:x[1], reverse=True))
    
    return chars_frequency

def plaintext_score(plaintext):
    score = 0
    
    strong = 3
    mid = 2
    low = 1

    common_substrings = {
        "the", "and", "ing", "ion", "ent", "her", "for", "tha", "nth", "int",
        "ere", "tio", "ter", "est", "ers", "ati", "hat", "ate", "all", "eth"
    }

    common_2_letter_words = {
        "am", "an", "as", "at", "be", "by", "do", "go", "he", "if",
        "in", "is", "it", "me", "my", "no", "of", "on", "or", "so",
        "to", "up", "us", "we"
    }

    # Check for 2 letter words
    for i in range(len(plaintext)-1):
        chunk = plaintext[i:i+2]
        if chunk in common_2_letter_words:
            score += strong

    # Check for 3 letter words
    for i in range(len(plaintext)-2):
        chunk = plaintext[i:i+3]
        if chunk in common_substrings:
            score += strong
    
    # Check for unexpected characters
    for c in plaintext:
        if c in letters_and_space:
            score += low
        elif c in punctuation:
            score += 0
        if c in impossible_chars:
            score -= strong
        # If char is not ASCII
        if ord(c) > 126:
            score -= mid
    

    # Frequency analysis of text
    chars_frequencies = frequency_analysis(plaintext)
    
    if chars_frequencies:
        top_char = next(iter(chars_frequencies))
        if top_char.lower() != "e":
            score -= mid

    return score


def decode_cipher(cipher: bytes):
    # These will be the returned data
    best_key = None
    best_score = float('-inf')
    best_plaintext = b""

    # We cycle through all possible byte values to find the key, create a same length as cipher key and xor it with the cipher
    for i in range(256):
        key = bytes([i])
        repeated_key = bytes([i])*len(cipher)
        result = fx.xor(cipher, repeated_key)
        try:
            decoded = result.decode('utf-8')
        except UnicodeDecodeError:
            continue
        score = plaintext_score(decoded)
        if score > best_score:
            best_key = key
            best_score = score
            best_plaintext = result

    return best_key, best_plaintext, best_score

if __name__ == "__main__":
    cipher = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")

    key, plaintext, score = decode_cipher(cipher)

    print(f"I thik the solution is {plaintext} with key = {key} and score = {score}")