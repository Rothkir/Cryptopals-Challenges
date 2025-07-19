import xor_cipher as xc

all_ciphers_solutions = {}

with open('4.txt', 'r', encoding='utf-8') as file:
    for cipher in file:
        key, plaintext, score = xc.decode_cipher(cipher=cipher)
        all_ciphers_solutions[key] = (plaintext, score)
        
all_ciphers_solutions = dict(sorted(all_ciphers_solutions.items(), key = lambda x:x[1][1], reverse=True))

key = next(iter(all_ciphers_solutions))
plaintext = all_ciphers_solutions[key][0]

print(key, plaintext)